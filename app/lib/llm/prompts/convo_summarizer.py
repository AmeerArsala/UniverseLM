# Given a conversation, summarize it while maintaining as much information as possible
from typing import Any, List, Dict

from langchain.prompts import ChatPromptTemplate
from langchain import hub

from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.messages import HumanMessage, AIMessage

from langchain.llms import HuggingFaceHub

from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser


# Prompt: Chain-of-Density
prompt = hub.pull("iamrobotbear/chain-of-density-prompt")


# LLM
LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=LLM_ID, model_kwargs={"temperature": 0.01, "max_length": 5000}
)


json_parser = SimpleJsonOutputParser()


# Chain inputs with defaults for all but {content}
# Usage: just pass in content (str)
"""
    content_category: Title Case, e.g., Article, Video Transcript, Blog Post, Research Paper.
    content: Content to summarize.
    entity_range: String range of how many entities to pick from the content and add to the summary.
    max_words: Summary maximum length in words.
    iterations: Number of entity densification rounds. Total summaries is iterations+1. For 80 words, 3 iterations is ideal. Longer summaries could benefit from 4-5 rounds, and also possibly sliding the entity_range to, e.g., 1-4.
"""
cod_chain_inputs = {
    "content": lambda d: d.get("content"),
    "content_category": lambda d: d.get("content_category", "Conversation"),
    "entity_range": lambda d: d.get("entity_range", "1-3"),
    "max_words": lambda d: int(d.get("max_words", 150)),
    "iterations": lambda d: int(d.get("iterations", 4)),
}


# 1st chain, showing intermediate results, can async stream
cod_streamable_chain = cod_chain_inputs | prompt | llm | json_parser

# Create the 2nd chain, for extracting the best summary only.
# Not streamable, we need the final result.
cod_final_summary_chain = cod_streamable_chain | (
    lambda output: output[-1].get(
        "denser_summary", 'ERR: No "denser_summary" key in last dict'
    )
)


def on_finish(summary: str):
    print(f"SUMMARY:\n{summary}")

    return summary


# Simplify this by just setting a variable `chain`
chain = cod_final_summary_chain | on_finish
