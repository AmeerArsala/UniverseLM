import os

from typing import List, Dict, Tuple, AsyncIterable, Awaitable
from enum import Enum

import faiss

from langchain_core.documents import Document
from langchain_community.docstore import InMemoryDocstore

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_community.llms import HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from app.constants import (
    OPENAI_MODEL,
    TEMP,
    OPENAI_EMBEDDINGS_MODEL,
    K_NEIGHBORS,
    HF_MODEL,
    encoder,
    HF_ENCODER_REPO_ID,
)

from app.lib.llm.chat_interface import Chat, RAGQAChat
from app.lib.llm.prompts import docrag


class ModelType(Enum):
    HUGGINGFACE = "HuggingFace"
    OPENAI = "OpenAI"
    GEMINI = "Gemini"


def get_embedding_model(model_type: ModelType):
    if model_type == ModelType.OPENAI:
        return OpenAIEmbeddings(model=OPENAI_EMBEDDINGS_MODEL)
    elif model_type == ModelType.HUGGINGFACE:
        return HuggingFaceEmbeddings(model_name=HF_ENCODER_REPO_ID)
    else:
        # return the sentence-transformer embeddings by default
        return HuggingFaceEmbeddings(model_name=HF_ENCODER_REPO_ID)


def create_retriever(
    embedder_type: ModelType, docs: List[Document], K: int = K_NEIGHBORS
):
    embeddings = get_embedding_model(embedder_type)

    vectordb = FAISS.from_documents(docs, embeddings)

    retriever = vectordb.as_retriever(search_kwargs=dict(k=K))

    return retriever


def get_llm_responder(
    llm_type: ModelType,
    temp: float = TEMP,
    stream_response: bool = True,
    verbose: bool = False,
):
    llm = None
    if llm_type == ModelType.HUGGINGFACE:
        llm = HuggingFaceEndpoint(
            endpoint_url=HF_MODEL,
            temperature=temp,
            streaming=stream_response,
            verbose=verbose,
        )
    elif llm_type == ModelType.OPENAI:
        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=temp,
            streaming=stream_response,
            verbose=verbose,
        )
    else:
        # Assume Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=temp,
            streaming=stream_response,
            verbose=verbose,
            convert_system_message_to_human=True,
        )

    return llm


def create_rag_chatbot(
    vectordb,
    openai_llm: str = OPENAI_MODEL,
    temp: float = TEMP,
    K: int = K_NEIGHBORS,
    stream_response: bool = True,
    verbose: bool = False,
    system_prompt: str = docrag.contextualize_q_system_prompt,
) -> RAGQAChat:

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temp,
        streaming=stream_response,
        verbose=verbose,
    )

    retriever = vectordb.as_retriever(search_kwargs=dict(k=K))

    return RAGQAChat(retriever, llm, system_prompt=system_prompt)
