from typing import List, Dict

from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)


# Prompting
# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
Your role is to summarize information that you are given about an entity that lives in a lore-rich society composed of entities, which refer to any of the following: individuals, groups of individuals, groups of groups, etc.
Given the entity's name and relevant context (which is composed of its existing entity profile, affiliation/group, lore involving said entity, and documents that belong to the entity), your summary should accurately describe the entity (as well as its role in the society). Your summary must be able to be used as an updated version of its existing user profile.
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


def stringify_lore(lore: List[str]) -> str:
    aggregated_lore: str = ""

    for i, lore_piece in enumerate(lore):
        aggregated_lore += f"""Lore Piece #{i+1}:
        {lore_piece}
        """

    return aggregated_lore


def stringify_belongings(belongings: List[str]) -> str:
    aggregated_belongings: str = ""

    for i, belonging in enumerate(belongings):
        aggregated_belongings += f"""Belonging/Document #{i+1}:
        {belonging}
        """

    return aggregated_belongings


def restring_affiliation(affiliation: str) -> str:
    if len(affiliation) > 0:
        return f"\n\nCONTEXT - AFFILIATION/GROUP OF ENTITY:\n{affiliation}"
    else:
        return ""


# Create the chain
chain = (
    RunnableParallel(
        {
            "profile": RunnablePassthrough(),
            "lore": RunnableLambda(stringify_lore),
            "belongings": RunnableLambda(stringify_belongings),
            "affiliation": RunnableLambda(restring_affiliation),
        }
    )
    | prompt
    | llm
)
