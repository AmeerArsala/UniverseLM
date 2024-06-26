import time

from typing import List, Dict, Tuple, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessageChunk

from app.lib.llm.prompts import docrag


class Chat:
    def __init__(
        self,
        response_model,
        system_prompt: str = "",
        chat_history: List[Tuple[str, str]] = [],
    ):
        self.chat_history = [("system", system_prompt), *chat_history]
        self.response_model = response_model
        self.chain = self._recreate_chain()

    def format_chat_history(self, include_system_prompt: bool = False) -> str:
        start_index = 0 if include_system_prompt else 1

        history: List = self.chat_history[start_index:]
        formatted_messages: List[str] = []
        for message in history:
            (owner, content) = message
            title: str = ""
            if owner == "human":
                title = "User"
            elif owner == "ai":
                title = "AI"

            formatted_msg: str = f"{title} - {content}"
            formatted_messages.append(formatted_msg)

        return "\n".join(formatted_messages)

    def _recreate_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [*self.chat_history, ("human", "{message}")]
        )

        chain = prompt | self.response_model | StrOutputParser()
        return chain

    def set_system_prompt(self, system_prompt: str):
        self.chat_history[0] = ("system", system_prompt)
        self.chain = self._recreate_chain()

    def add_to_chat_history(self, message_s: List[Tuple[str, str]]):
        for message in message_s:
            self.chat_history.append(message)

        self.chain = self._recreate_chain()

    def invoke_chat(
        self,
        inputs: Dict[str, str],
        add_to_history: bool = True,
    ):
        invocation: str = self.chain.invoke(inputs)

        if add_to_history:
            self.add_to_chat_history([("human", inputs["message"]), ("ai", invocation)])

        return invocation


class RAGQAChat(Chat):
    def __init__(
        self,
        retriever,
        response_model,
        system_prompt: str = docrag.SYSTEM_PROMPT,
        human_prompt: str = docrag.HUMAN_PROMPT,
        chat_history: List[Tuple[str, str]] = [],
        recontextualize_if_chat_history: bool = False,
    ):
        self.retriever = retriever
        self.human_prompt = human_prompt
        self.recontextualize_if_chat_history = recontextualize_if_chat_history
        super().__init__(response_model, system_prompt, chat_history)

    def format_docs(docs: List):
        return "\n\n".join(doc.page_content for doc in docs)

    def _make_contextualize_question_chain(self):
        (system_prompt, msg_history) = (self.chat_history[0], self.chat_history[1:])

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", docrag.contextualize_q_system_prompt),
                *msg_history,
                ("human", self.human_prompt),
            ]
        )

        contextualize_q_chain = (
            contextualize_q_prompt | self.response_model | StrOutputParser()
        ).with_config(tags=["contextualize_q_chain"])

        return contextualize_q_chain

    def _recreate_chain(self):
        prompt = ChatPromptTemplate.from_messages(
            [*self.chat_history, ("human", self.human_prompt)]
        )

        rag_chain_from_docs = None

        # more messages than just the system prompt is needed for this to be True
        if self.recontextualize_if_chat_history and len(self.chat_history) > 1:
            # Contextualize the question
            contextualize_q_chain = self._make_contextualize_question_chain()

            rag_chain_from_docs = (
                RunnablePassthrough.assign(
                    # format docs after retrieving
                    context=(lambda x: RAGQAChat.format_docs(x["context"])),
                    question=contextualize_q_chain,
                )
                | prompt
                | self.response_model
                | StrOutputParser()
            )
        else:
            rag_chain_from_docs = (
                RunnablePassthrough.assign(
                    # format docs after retrieving
                    context=(lambda x: RAGQAChat.format_docs(x["context"]))
                )
                | prompt
                | self.response_model
                | StrOutputParser()
            )

        rag_chain_with_sources = RunnableParallel(
            {
                "context": RunnableLambda(lambda x: x["question"]) | self.retriever,
                "question": RunnableLambda(lambda x: x["question"]),
            }
        ).assign(answer=rag_chain_from_docs)

        return rag_chain_with_sources

    def invoke_chat(
        self, inputs: Dict[str, str], add_to_history: bool = True
    ) -> Dict[str, str]:
        invocation = self.chain.invoke(inputs)

        if add_to_history:
            self.add_to_chat_history(
                [("human", inputs["question"]), ("ai", invocation["answer"])]
            )

        return invocation

    # TODO: have it update the buffer every single time so it can store the memories
    async def generate_chat_response_events(
        self,
        msg,
        add_to_history: bool = True,
        sleep_time: float = 0.1,
        print_chunks: bool = False,
    ):
        # Initialize a flag to track if any data was yielded
        data_yielded = False

        response: str = ""

        # response_buffer: str = ""
        async for chunk in self.chain.astream(msg):
            print(f"\nCHUNK: {chunk}\n")

            chunk_text: str = chunk.get("answer")
            if chunk_text is None:
                chunk_docs = chunk.get("context")

                if chunk_docs is None:
                    # that means it's the question, which we don't care about
                    continue
                else:
                    chunk_text = "".join([doc.page_content for doc in chunk_docs])

            response += chunk_text

            if print_chunks:
                print(chunk_text, end="")

            data_yielded = True  # Indicate that data was yielded

            chunk_content_html: str = chunk_text.replace("\n", "<br>")
            yield f"data: {chunk_content_html}\n\n"

            if sleep_time > 0:
                time.sleep(sleep_time)

        # Check if any data was yielded
        if not data_yielded:
            # onFinish
            print("Streaming complete")

            if add_to_history:
                self.add_to_chat_history([("human", msg), ("ai", response)])
