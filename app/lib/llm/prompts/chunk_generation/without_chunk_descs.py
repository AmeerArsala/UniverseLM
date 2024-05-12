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
import json


# COMMUNITY DESC GENERATION CHAIN
# (count) -> community_desc: str

# TODO: GPT-orchestration (p-tuning) + few-shot this
community_system_prompt_message = """
Your role is to describe what a society is like given the individuals, groups, groups of groups, etc. that inhabit it. Given a specified number of entities (which refer to individuals, groups of individuals, groups of groups, etc.), you must generate an accurate all-encompassing big-picture description of said society. Be creative here but try to be accurate, as a small number of entities should not be in a society described for its vastness.
"""[
    1:-1
]

COMMUNITY_DESC_HUMAN_PROMPT = """
NUM ENTITIES: {num_entities}
"""

community_desc_prompt = ChatPromptTemplate.from_messages(
    [("system", community_system_prompt_message), ("human", COMMUNITY_DESC_HUMAN_PROMPT)]
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
community_desc_chain = (community_desc_prompt | community_desc_llm)


# CHUNK DESC GENERATION CHAIN
# (count, community_desc) -> List[Chunk]
# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
Your role is to generate profiles for entities in a given community. Given a description of what the community is like as well as the number of entities (an entity can be a single individual, a group of individuals, a group of groups, etc.), you are to generate full profiles for each entity. Each profile must consist of:
    - Name: name of entity (which may refer to an individual, a group, a group of groups, etc.)
    - Description: complete description of entity as it relates to the community as a whole.
    - Affiliation: name of entity that it is affiliated with/belongs to (if an individual belonged to a group for example, they would be 'affiliated' with the name of the entity that represents said group). If no affiliation (not required), put 'NONE'

You must respond in a JSON format, with the keys to each object being the 3 bullet points up above.
"""[
    1:-1
]

HUMAN_PROMPT = """
COMMUNITY DESCRIPTION:
{community_desc}

NUMBER OF ENTITIES: {num_chunks}
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

    output: str = ai_message.content

    # Given the output of the llm and a `community_id`, parse into a List[Chunk]
    chunk_dicts: List[Dict] = json.loads(output)

    # TODO: The LLM must be gaslighted into returning a list of dicts as described below
    chunks = [
        Chunk(
            name=chunk_dict["name"],
            profile=chunk_dict["description"],
            community_id=community_id,
            parent_chunk=chunk_dict["affiliation"],
        )
        for chunk_dict in chunk_dicts
    ]

    return chunks


def dynamic_route(info: Dict):
    inputs: Dict[str, str] = {
        "num_chunks": info["num_chunks"],
        "community_desc": info["community_desc"],
    }

    def parse_output(ai_message: AIMessage) -> List[Chunk]:
        community_id: int = info["community_id"]

        return parse_chunks(ai_message, community_id)

    return inputs | prompt | llm | parse_output


# Create the chain
chain = RunnableParallel(
    {
        "num_chunks": RunnablePassthrough(),
        "community_desc": RunnablePassthrough(),
        "community_id": RunnablePassthrough(),
    }
) | RunnableLambda(dynamic_route)
