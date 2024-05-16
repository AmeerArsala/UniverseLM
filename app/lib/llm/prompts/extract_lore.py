# Extract information to memorize in lore
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser


# Prompting
# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
Your role is to determine which piece of information to memorize as a record. Given a piece of info and context about the user/the conversation, you are to determine which of this information you should memorize. Your output should reflect what new key information was learned.
In general, you should be memorizing information if:
(A) The information given the context is actually a key piece of information (and not just filler) that is genuinely important to the matter at hand. If this were a fictional world, the information worth memorizing would essentially be important lore. 
(B) The user might say exactly to memorize something, in which case you SHOULD memorize it 
"""[
    1:-1
]

HUMAN_PROMPT = """
CONTEXT:
{context}

INFO:
{info}
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), ("human", HUMAN_PROMPT)]
)

# LLM
LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 500}
)


# Create the chain
chain = prompt | llm | StrOutputParser()

# ----------------------------------------------------------------------------------------
# TODO: GPT-orchestration (p-tuning) + few-shot this

about_system_prompt_message = """
Your role is to determine which entities are being referred to within a given piece of information, given context and a list of entities. You are to return a list of these names as a Python list and nothing else.
Your list should represent the entities that are the subjects of the given piece of information (given the context).
"""[
    1:-1
]

ABOUT_HUMAN_PROMPT = """
ENTITIES:
{entities}

CONTEXT:
{context}

INFO:
{info}
"""

about_prompt = ChatPromptTemplate.from_messages(
    [("system", about_system_prompt_message), ("human", ABOUT_HUMAN_PROMPT)]
)


# LLM
ABOUT_LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
about_llm = HuggingFaceHub(
    repo_id=ABOUT_LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 500}
)


# Create the chain
about_chain = about_prompt | about_llm | StrOutputParser()
