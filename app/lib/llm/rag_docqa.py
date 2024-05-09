from typing import List, Dict, Tuple, AsyncIterable, Awaitable
from enum import Enum

import faiss

from langchain_core.documents import Document
from langchain_community.docstore import InMemoryDocstore

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_community.llms import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI, OpenAI


from app.constants import (
    OPENAI_MODEL,
    TEMP,
    K_NEIGHBORS,
    HF_MODEL,
    encoder,
    encoder_repo_id,
)
from app.lib.llm.chat_interface import Chat, RAGQAChat
from app.lib.llm.prompts import sysprompts


class ModelType(Enum):
    HUGGINGFACE = "HuggingFace"
    OPENAI = "OpenAI"


def get_embedding_model(model_type: ModelType):
    if model_type == ModelType.OPENAI:
        return OpenAIEmbeddings(model="text-embedding-ada-002")
    elif model_type == ModelType.HUGGINGFACE:
        return HuggingFaceEmbeddings(model_name=encoder_repo_id)


def create_rag_chatbot(
    vectordb,
    openai_llm: str = OPENAI_MODEL,
    temp: float = TEMP,
    K: int = K_NEIGHBORS,
    stream_response: bool = True,
    verbose: bool = False,
    system_prompt: str = sysprompts.contextualize_q_system_prompt,
) -> RAGQAChat:

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temp,
        streaming=stream_response,
        verbose=verbose,
    )

    retriever = vectordb.as_retriever(search_kwargs=dict(k=K))

    return RAGQAChat(retriever, llm, system_prompt=system_prompt)
