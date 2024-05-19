from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

import anyio

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore

from app.core.db import database as db
import sqlalchemy

from app.lib.llm.chat_interface import RAGQAChat

from app.lib.llm.prompts import sysprompts
from app.lib.llm.prompts.sysprompts import AgentSystemPrompt
from app.lib.llm.prompts import (
    confirm_memorize,
    extract_lore,
    loreworthy,
    convo_summarizer,
)

from app.lib.llm.rag import ModelType, create_retriever, get_llm_responder

from app.lib import society, states

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser


class AgentChatParams(BaseModel):
    question: str
    sender_chunk_name: str


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
        **kwargs,
    ):
        self.community_id = community_id
        self.chunk_name = chunk_name
        self.agent_sys_prompt = AgentSystemPrompt(NAME=chunk_name, DESC=agent_desc)

        system_prompt: str = self.agent_sys_prompt.rag_prompt()
        human_prompt: str = sysprompts.HUMAN_PROMPT

        super().__init__(
            retriever,
            response_model,
            system_prompt,
            human_prompt,
            chat_history,
            recontextualize_if_chat_history,
        )

        known_chunk_names = self._getknownchunks()
        if known_chunk_names is None or self.chunk_name not in known_chunk_names:
            # Refresh the known chunks, because this agent wouldn't exist without it being in the DB
            states.refresh_known_chunks(self.community_id)

        # self.chatbot_kwargs = kwargs

    def _getknownchunks(self) -> List[str]:
        return states.known_chunks.get(self.community_id)

    def update_retriever(self):
        docs: List[Document] = states.community_states[self.community_id].to_docs()
        embedder_type: ModelType = ModelType.HUGGINGFACE  # for now

        self.retriever = create_retriever(embedder_type, docs)

    def format_chat_history(
        self, sender_chunk_name: str = "User", include_system_prompt: bool = False
    ) -> str:
        start_index = 0 if include_system_prompt else 1

        if start_index > len(self.chat_history) - 1:
            return ""

        history: List = self.chat_history[start_index:]
        formatted_messages: List[str] = []
        for message in history:
            (owner, content) = message
            title: str = ""
            if owner == "human":
                title = sender_chunk_name
            elif owner == "ai":
                title = self.chunk_name

            formatted_msg: str = f"{title}: {content}"
            formatted_messages.append(formatted_msg)

        return "\n".join(formatted_messages)

    def attempt_lore_update(self, params: Dict):
        print("Attempting lore update...")

        message: str = params["question"]
        sender_chunk_name: str = params["sender_chunk_name"]

        formatted_chat_history: str = self.format_chat_history(
            include_system_prompt=False, sender_chunk_name=sender_chunk_name
        )

        print("Summarizing chat history...")
        summarized_chat_history: str = (
            ""
            if formatted_chat_history == ""
            else convo_summarizer.chain.invoke({"content": formatted_chat_history})
        )

        new_info: str = f"{sender_chunk_name} - {message}"

        # (A) Find out whether this needs to be stored as Lore
        # Is the info key info that you need to memorize? Is the user asking you to remember it?
        print("Deciding whether to memorize info...")
        should_memorize: bool = confirm_memorize.chain.invoke(
            {
                "context": summarized_chat_history,
                "info": new_info,
                "community_id": self.community_id,
            }
        )

        if should_memorize:
            print("Memorizing...")

            extracted_lore: Dict = extract_lore.chain.invoke(
                {
                    "possible_entities": self._getknownchunks(),
                    "context": summarized_chat_history,
                    "info": new_info,
                }
            )

            if extracted_lore["valid_output"]:
                extracted_lore: Lore = Lore(
                    lore_text=extracted_lore["extracted_info"],
                    about_chunks=extracted_lore["about_entities"],
                )

                society.upload_lore([extracted_lore], community_id=self.community_id)
            else:
                print("On second thought, don't memorize")

        # (B) Re-profile the chunk based on the new info if new enough
        # Does the info change the view of the user enough to justify re-profiling?
        print("Deciding whether to reprofile...")
        should_reprofile: bool = False  # TODO: change later

        if should_reprofile:
            print("Reprofiling...")
            # First of all, the question that needs to be answered here is: WHO to reprofile?

            def update_profile(chunk_name: str):
                chunk_summary: str = society.summarize_chunk(chunk_name)
                society.set_profile(self.community_id, chunk_name, chunk_summary)
                self.agent_sys_prompt.DESC = chunk_summary  # SELF??? Nah fix this later

            update_profile(sender_chunk_name)

    # Dynamic routing; happens at the call level
    # Returns a chain
    def agent_route(self, params: Dict):
        # Question can be just a message
        message: str = params["question"]

        # Make sure to set who the sender is so the agent knows
        self.agent_sys_prompt.recipient = params["sender_chunk_name"]
        # print(self.agent_sys_prompt.recipient)

        # Attempt to update the lore of the society given new information from the conversation
        # Allowing other agents to feel the effects and behave differently as the overall lore is updated
        self.attempt_lore_update(params)

        # Find out whether some type of lore retrieval is needed [Retrieve from lore and belongings]
        # Is the user asking a question that may require knowledge of Lore?
        # TODO: change this so it's not always True
        print("Deciding whether query warrants retrieval...")
        lore_ragworthy: bool = True  # loreworthy.chain.invoke({"input": message})

        if lore_ragworthy:
            print("Retrieving relevant info and responding...")

            # Update retriever
            self.update_retriever()

            return super()._recreate_chain()
        else:
            print("No need for retrieval. Responding normally...")

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
        full_chain = RunnablePassthrough.assign(
            sender_chunk_name=(lambda x: x["sender_chunk_name"]),
            # context=(lambda x: x["context"]),
            question=(lambda x: x["question"]),
        ) | RunnableLambda(self.agent_route)

        return full_chain

    async def generate_chat_response_events(
        self,
        chat_params: Dict,
        add_to_history: bool = True,
        sleep_time: float = 0.1,
        print_chunks: bool = False,
    ):
        super().generate_chat_response_events(
            chat_params, add_to_history, sleep_time, print_chunks
        )


chats: Dict[str, AgentChat] = {}


# Assumes the chunk is already in the DB
def create_chat(community_id: int, chunk_name: str, **kwargs) -> AgentChat:
    with db.engine.begin() as conn:
        results = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM chunks WHERE community_id = :community_id AND name = :name"
            ),
            [{"community_id": community_id, "name": chunk_name}],
        )

        chunk: Chunk = Chunk.wrap_result(results.first())

        # Generate retriever
        docs: List[Document] = states.community_states[community_id].to_docs()
        embedder_type: ModelType = ModelType.HUGGINGFACE  # for now

        retriever = create_retriever(embedder_type, docs)

        # Get response model
        llm_type: ModelType = ModelType.COHERE  # try gemini as the default
        response_model = get_llm_responder(llm_type, **kwargs)

        # Get agent desc
        agent_desc: str = chunk.profile

        chat: AgentChat = AgentChat(
            retriever=retriever,
            response_model=response_model,
            chunk_name=chunk.name,
            agent_desc=agent_desc,
            community_id=chunk.community_id,
            **kwargs,
        )

    return chat


def manifest_chat(community_id: int, chunk_name: str, **kwargs) -> AgentChat:
    global chats

    chat_id: str = f"{community_id}::{chunk_name}"

    chat = chats.get(chat_id)

    if chat is None:
        # Make a new one
        chat = create_chat(community_id, chunk_name, **kwargs)
        chats[chat_id] = chat

    return chat
