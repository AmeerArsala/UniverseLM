from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

from app.core.schemas.entities import Chunk

from app.core.db import database as db
import sqlalchemy

from app.lib.llm.chat_interface import RAGQAChat

from app.lib.llm.prompts import sysprompts
from app.lib.llm.prompts.sysprompts import AgentSystemPrompt
from app.lib.llm.prompts import confirm_memorize, extract_lore, loreworthy

from app.lib.society import upload_lore, summarize_chunk, profile

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableParallel,
)

from langchain_core.output_parsers import StrOutputParser


# Create an interface for chatting with the agents
class AgentChat(RAGQAChat):
    def __init__(
        self,
        retriever,
        response_model,
        chunk_name: str,
        agent_desc: str,
        chat_history: List[Tuple[str, str]] = [],
        recontextualize_if_chat_history: bool = False,
    ):
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

    # Dynamic routing; happens at the call level
    # Returns a chain
    def agent_route(self, info: Dict):
        # Question can be just a message
        message: str = info["question"]

        # (A) Find out whether this needs to be stored as Lore
        # Is the info key info that you need to memorize? Is the user asking you to remember it?
        memorization_input: str = f"""
        CONTEXT:
        {self.format_chat_history(include_system_prompt=False)}
        
        INFO:
        {message}
        """
        should_memorize: bool = confirm_memorize.chain.invoke(
            {"input": memorization_input}
        )

        if should_memorize:
            print("Memorizing...")
            extracted_lore: str = extract_lore.chain.invoke(
                {"input": memorization_input}
            )
            upload_lore(extracted_lore)

        # (B) Re-profile the user based on the new info if new enough
        # Does the info change the view of the user enough to justify re-profiling?
        should_reprofile: bool = should_memorize  # change later

        if should_reprofile:
            print("Reprofiling...")
            profile(self.chunk_name, summarize_chunk(self.chunk_name))

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
            "chunk_name": RunnablePassthrough(),
            "context": RunnablePassthrough(),
            "question": RunnablePassthrough(),  # it honestly doesn't have to be a question, but there for simplicity
        } | RunnableLambda(self.agent_route)

        return full_chain


chats: Dict[str, AgentChat] = {}


# TODO:
# Assumes the chunk is already in the DB
def create_chat(chunk_name: str) -> AgentChat:
    with db.engine.begin() as conn:
        results = conn.execute(
            sqlalchemy.text(
                "SELECT * FROM chunks WHERE name = :name", [{"name": chunk_name}]
            )
        )

        chunk: Chunk = [Chunk.wrap_result(result) for result in results][0]

        # Generate retriever
        retriever = None

        # Get response model
        response_model = None

        # Get agent desc
        agent_desc: str = ""

        chat: AgentChat = AgentChat(
            retriever=retriever,
            response_model=response_model,
            chunk_name=chunk_name,
            agent_desc=agent_desc,
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
