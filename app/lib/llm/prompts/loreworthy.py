# (C) Find out whether some type of RAG is needed [Retrieve from lore and belongings]
# Is the user asking a question that may require knowledge of Lore?
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub

from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage


# Load environment variables
load_dotenv()


# Prompting
system_prompt_message = """
You live in a society that is filled with lore. Your role is to determine whether or not you should reach into that lore to find relevant information in order to respond to something in a conversation. Given a message from the user, you are to determine whether you need additional context by returning either "CONTEXTUALIZE" (for additional context/lore) or "VANILLA" (for no additional context needed, such as the user asking what 2 + 2 is). Do not say anything more.
"""[
    1:-1
]

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), ("human", "{input}")]
)

# LLM
LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 500}
)


def parse_output(ai_message: AIMessage, default_response=True) -> bool:
    content: str = ai_message.content

    content_len: int = len(content)
    vanilla_len: int = len("VANILLA")
    contextualize_len: int = len("CONTEXTUALIZE")

    if (
        content_len >= contextualize_len
        and content[:contextualize_len].upper() == "CONTEXTUALIZE"
    ):
        return True
    elif content_len >= vanilla_len and content[:vanilla_len].upper() == "VANILLA":
        return False
    else:
        return default_response


# Create the chain
chain = prompt | llm | parse_output
