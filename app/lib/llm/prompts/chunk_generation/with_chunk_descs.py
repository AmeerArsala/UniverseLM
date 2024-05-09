from typing import List, Dict

from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)

from langchain_core.messages import AIMessage
from app.core.schemas.entities import Chunk


# COMMUNITY DESC GENERATION CHAIN
# (lazy_chunk_descs[str]) -> community_desc: str

# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
Your role is 
"""[
    1:-1
]

COMMUNITY_DESC_HUMAN_PROMPT = """
ENTITY NAME: {name}

CONTEXT - EXISTING ENTITY PROFILE:
{profile}{affiliation}

CONTEXT - LORE INVOLVING ENTITY:
{lore}

CONTEXT - DOCUMENTS BELONGING TO ENTITY:
{belongings}
"""

community_desc_prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), ("human", COMMUNITY_DESC_HUMAN_PROMPT)]
)

# LLM
COMMUNITY_DESC_LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
community_desc_llm = HuggingFaceHub(
    repo_id=COMMUNITY_DESC_LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 500}
)


def stringify_lazy_chunks(lazy_chunk_descs: List[str]) -> str:
    aggregated_chunks: str = ""

    for i, lazy_chunk_desc in enumerate(lazy_chunk_descs):
        aggregated_chunks += f"""Entity #{i+1} - Description:
        {lazy_chunk_desc}
        """

    return aggregated_chunks


# Create the chain
community_desc_chain = (
    RunnableParallel({"lazy_chunk_descs": RunnableLambda(stringify_lazy_chunks)})
    | community_desc_prompt
    | community_desc_llm
)


# CHUNK DESC GENERATION CHAIN
# (lazy_chunk_descs[], community_desc) -> List[Chunk]
# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
Your role is 
"""[
    1:-1
]

HUMAN_PROMPT = """
ENTITY NAME: {name}

CONTEXT - EXISTING ENTITY PROFILE:
{profile}{affiliation}

CONTEXT - LORE INVOLVING ENTITY:
{lore}

CONTEXT - DOCUMENTS BELONGING TO ENTITY:
{belongings}
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), ("human", HUMAN_PROMPT)]
)


# LLM
LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 500}
)


def parse_chunks(ai_message: AIMessage, community_id: int) -> List[Chunk]:
    chunks: List[Chunk] = []

    content: str = ai_message.content

    # TODO: parse chunks
    # Given the output of the llm and a `community_id`, parse into a List[Chunk]

    return chunks


def dynamic_route(info: Dict):
    inputs: Dict = {
        "lazy_chunk_descs": info["lazy_chunk_descs"],
        "community_desc": info["community_desc"],
    }

    def parse_output(ai_message: AIMessage) -> List[Chunk]:
        community_id: int = info["community_id"]

        return parse_chunks(ai_message, community_id)

    return inputs | prompt | llm | parse_output


# Create the chain
chain = RunnableParallel(
    {
        "lazy_chunk_descs": RunnableLambda(stringify_lazy_chunks),
        "community_desc": RunnablePassthrough(),
        "community_id": RunnablePassthrough(),
    }
) | RunnableLambda(dynamic_route)