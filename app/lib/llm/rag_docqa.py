# NOTE: make sure to use langchain_community with the HF stuff, because importing from straight up langchain will be deprecated
from typing import List, Dict, Tuple, AsyncIterable, Awaitable

# import asyncio

import kdbai_client as kdbai

# from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import KDBAI
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

from app.lib.llm.chat_interface import Chat, RAGQAChat
from app.lib.llm.prompts import sysprompts

# from langchain.schema import HumanMessage


# Options
# gpt-4-turbo-2024-04-09
# gpt-3.5-turbo-0125
# gpt-3.5-turbo-instruct
OPENAI_MODEL = "gpt-4-turbo-2024-04-09"
TEMP = 0.5
K_NEIGHBORS = 3

SYSTEM_PROMPT = sysprompts.SYSTEM_PROMPT


def get_embedding_model():
    # TODO: change to a different embedding model
    return OpenAIEmbeddings(model="text-embedding-ada-002")


def get_doc_uid(unique_doc_id: str) -> str:
    return "txtchunks_" + unique_doc_id.replace(".", "_")


def create_ragbot_from_vectordb(
    vectordb,
    openai_llm: str = OPENAI_MODEL,
    temp: float = TEMP,
    K: int = K_NEIGHBORS,
    stream_response: bool = True,
    verbose: bool = False,
):
    # Create the chain
    qabot = RetrievalQA.from_chain_type(
        chain_type="stuff",
        llm=ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=temp,
            streaming=stream_response,
            verbose=verbose,
        ),
        retriever=vectordb.as_retriever(search_kwargs=dict(k=K)),
        return_source_documents=True,
    )

    return qabot


def create_rag_chatbot_from_vectordb(
    vectordb,
    openai_llm: str = OPENAI_MODEL,
    temp: float = TEMP,
    K: int = K_NEIGHBORS,
    stream_response: bool = True,
    verbose: bool = False,
) -> RAGQAChat:

    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=temp,
        streaming=stream_response,
        verbose=verbose,
    )

    retriever = vectordb.as_retriever(search_kwargs=dict(k=K))

    return RAGQAChat(retriever, llm, system_prompt=SYSTEM_PROMPT)


# for unique_doc_name, you can just make it the arxiv id
def create_rag_chatbot(
    unique_doc_id: str, text_chunks: List[str], session: kdbai.Session, **kwargs
):
    schema = {
        "columns": [
            {"name": "id", "pytype": "str"},
            {"name": "text", "pytype": "bytes"},
            {
                "name": "embeddings",
                "pytype": "float32",
                "vectorIndex": {"dims": 1536, "metric": "L2", "type": "hnsw"},
            },
        ]
    }

    doc_uid: str = get_doc_uid(unique_doc_id)

    table = session.create_table(doc_uid, schema)

    embeddings = get_embedding_model()

    vectordb = KDBAI(table, embeddings)
    vectordb.add_texts(texts=text_chunks)

    return create_rag_chatbot_from_vectordb(
        vectordb, openai_llm=OPENAI_MODEL, temp=TEMP, K=K_NEIGHBORS, **kwargs
    )


def manifest_rag_chatbot(
    unique_doc_id: str, session: kdbai.Session, text_chunks=None, **kwargs
):
    # Attempt to find it, if not found, create a new one

    try:
        print("Finding vector DB table...")

        table = session.table(get_doc_uid(unique_doc_id))

        embeddings = get_embedding_model()

        vectordb = KDBAI(table, embeddings)

        return create_rag_chatbot_from_vectordb(
            vectordb, openai_llm=OPENAI_MODEL, temp=TEMP, K=K_NEIGHBORS, **kwargs
        )
    except Exception as err:  # KDBAIException
        print("Vector DB table not found. Creating new...")

        # Make a new one
        return create_rag_chatbot(unique_doc_id, text_chunks, session, **kwargs)
