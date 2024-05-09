# (B) Find out whether this needs to be stored as Lore
# Is the info key info that you need to memorize? Is the user asking you to remember it?
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage


# Load environment variables
load_dotenv()


# Prompting
system_prompt_message = """
Your role is to determine whether you should memorize a piece of information or not. Given a piece of info and context about the user/the conversation, you are to determine whether you should memorize this information or not by returning either "YES" or "NO". Do not say anything more.
In general, you should be memorizing information if:
(A) The information given the context is actually a key piece of information (and not just filler) that is genuinely important to the matter at hand. If this were a fictional world, the information worth memorizing would essentially be important lore. 
(B) They might say exactly to memorize something (in which case the answer is obviously yes)
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


def parse_output(ai_message: AIMessage) -> bool:
    content: str = ai_message.content

    if len(content) > 2:
        return content[:3].upper() == "YES"
    else:
        return content[:2].upper() == "NO"


# Create the chain
chain = prompt | llm | parse_output
