from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

# import asyncio

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore

from app.core.db import database as db
import sqlalchemy

from app.lib.llm.chat_interface import RAGQAChat

from app.lib.llm.prompts import sysprompts
from app.lib.llm.prompts.sysprompts import AgentSystemPrompt
from app.lib.llm.prompts import confirm_memorize, extract_lore, loreworthy

from app.lib import society, states

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser


# Create an interface for chatting with the agents
class AgentChat(RAGQAChat):
    def __init__(
        self,
        retriever,
        response_model,
        chunk_name: str,
        agent_desc: str,
        community_id: int,
        chat_history: List[Tuple[str, str]] = [],
        recontextualize_if_chat_history: bool = False,
    ):
        self.community_id = community_id
        self.chunk_name = chunk_name
        self.agent_sys_prompt = AgentSystemPrompt(DESC=agent_desc)
        system_prompt: str = self.agent_sys_prompt.rag_prompt()

        super().__init__(
            retriever,
            response_model,
            system_prompt,
            chat_history,
            recontextualize_if_chat_history,
        )

        known_chunk_names = self._getknownchunks()
        if known_chunk_names is None or self.chunk_name not in known_chunk_names:
            # Refresh the known chunks, because this agent wouldn't exist without it being in the DB
            states.refresh_known_chunks(self.community_id)

    def _getknownchunks(self) -> List[str]:
        return states.known_chunks.get(self.community_id)

    # Dynamic routing; happens at the call level
    # Returns a chain
    def agent_route(self, params: Dict):
        # Question can be just a message
        message: str = params["question"]
        formatted_chat_history: str = self.format_chat_history(
            include_system_prompt=False
        )

        # (A) Find out whether this needs to be stored as Lore
        # Is the info key info that you need to memorize? Is the user asking you to remember it?
        should_memorize: bool = confirm_memorize.chain.invoke(
            {"context": formatted_chat_history, "info": message}
        )

        if should_memorize:
            print("Memorizing...")
            extracted_lore_text: str = extract_lore.chain.invoke(
                {"context": formatted_chat_history, "info": message}
            )

            subject_chunks: List[str] = extract_lore.about_chain.invoke(
                {
                    "context": formatted_chat_history,
                    "info": extracted_lore_text,
                    "entities": "\n".join(self._getknownchunks()),
                }
            )

            extracted_lore: Lore = Lore(
                lore_text=extracted_lore_text, about_chunks=subject_chunks
            )
            society.upload_lore(extracted_lore, community_id=self.community_id)

        # (B) Re-profile the chunk based on the new info if new enough
        # Does the info change the view of the user enough to justify re-profiling?
        should_reprofile: bool = should_memorize  # change later

        if should_reprofile:
            print("Reprofiling...")

            async def update_profile(chunk_name: str):
                chunk_summary: str = await society.summarize_chunk(chunk_name)
                society.set_profile(self.community_id, chunk_name, chunk_summary)
                self.agent_sys_prompt.DESC = chunk_summary

            update_profile(params["sender_chunk_name"])

        # (C) Find out whether some type of RAG is needed [Retrieve from lore and belongings]
        # Is the user asking a question that may require knowledge of Lore?
        rag: bool = loreworthy.chain.invoke({"input": message})

        if rag:
            return super()._recreate_chain()
        else:
            # Just use regular language model + prompting
            nonrag_sys_prompt: str = self.agent_sys_prompt.nonrag_prompt()
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", nonrag_sys_prompt),
                    *self.chat_history[1:],
                    ("human", "{question}"),
                ]
            )

            return prompt | self.response_model | StrOutputParser()

    def _recreate_chain(self):
        full_chain = {
            "sender_chunk_name": RunnablePassthrough(),
            "context": RunnablePassthrough(),
            "question": RunnablePassthrough(),  # it honestly doesn't have to be a question, but there for simplicity
        } | RunnableLambda(self.agent_route)

        return full_chain


chats: Dict[str, AgentChat] = {}


# TODO:
# Assumes the chunk is already in the DB
def create_chat(community_id: int, chunk_name: str) -> AgentChat:
    with db.engine.begin() as conn:
        results = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM chunks WHERE community_id = :community_id AND name = :name",
                [{"community_id": community_id, "name": chunk_name}],
            )
        )

        chunk: Chunk = Chunk.wrap_result(results.first())

        # Generate retriever
        retriever = None

        # Get response model
        response_model = None

        # Get agent desc
        agent_desc: str = chunk.profile

        chat: AgentChat = AgentChat(
            retriever=retriever,
            response_model=response_model,
            chunk_name=chunk.name,
            agent_desc=agent_desc,
            community_id=chunk.community_id,
        )

        chats[chunk_name] = chat

    return chat


def manifest_chat(chunk_name: str) -> AgentChat:
    global chats

    chat = chats.get(chunk_name)

    if chat is None:
        # Make a new one
        chat = create_chat(chunk_name)

    return chat
