# Extract information to memorize in lore
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub


# Prompting
system_prompt_message = """
Your role is to determine which piece of information to memorize as a record. Given a piece of info and context about the user/the conversation, you are to determine which of this information you should memorize. Your output should reflect what new key information was learned.
In general, you should be memorizing information if:
(A) The information given the context is actually a key piece of information (and not just filler) that is genuinely important to the matter at hand. If this were a fictional world, the information worth memorizing would essentially be important lore. 
(B) The user might say exactly to memorize something, in which case you SHOULD memorize it 
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


# Create the chain
chain = prompt | llm
