# (B) Find out whether this needs to be stored as Lore
# Is the info key info that you need to memorize? Is the user asking you to remember it?
from typing import Any, List, Dict

from langchain.prompts import ChatPromptTemplate, PromptTemplate

from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.messages import HumanMessage, AIMessage

from langchain.llms import HuggingFaceHub
from langchain_cohere import ChatCohere
from app.lib.llm.prompts import convo_summarizer

from langchain_core.output_parsers import StrOutputParser

from app.lib.llm.chat_interface import RAGQAChat
from app.lib.llm.rag import ModelType
from app.lib import states


# Prompting
Q1: str = (
    "Did the user explicitly express intent that they want you to memorize/remember a piece of information?"
)
Q2: str = (
    "Is the new given information actually new information that you haven't heard before / wasn't obvious (such as a new event)? That is, if you were to tell a story about the information you've heard, would this be included as lore in the story?"
)
Q3: str = (
    "Does the given information change one's perspective on prior information? Does there exist any information within the new information that adds anything meaningful?"
)

# TODO: p-tune this
system_prompt_message = (
    """
You are a recordkeeper who records important information. Your role is to determine whether information is important or not by answering a few questions. Given a piece of info and context about the user/the conversation, you are to answer a few questions with either "YES" or "NO" (and nothing more) that will determine the importance of the info.
In general, you should be considering information important if:
(A) The information given the context is actually a key piece of information (and not just filler) that is genuinely important to the matter at hand. If this were a fictional world, the information worth memorizing would essentially be important lore or new events that occur. 
(B) They might say exactly to memorize something

As you answer the questions, use the following pieces of retrieved additional relevant context delimited by XML tags.
<retrieved context>
Retrieved Additional Context:
{retrieved_context}
</retrieved context>
"""
    + f"""
Here are the questions you must answer:
1. {Q1}
2. {Q2}
3. {Q3} 
"""[
        1:
    ]
)

HUMAN_PROMPT = """CONTEXT:
{context}

INFO:
{info}
"""

few_shot_examples: List = [
    HumanMessage(
        content="""CONTEXT:
<NOTHING/>

INFO:
what is 1 + 1
"""
    ),
    AIMessage(
        content=f"""<QA>
Q1: {Q1}
A1: NO

Q2: {Q2}
A2: NO

Q4: {Q3}
A3: NO
</QA>"""
    ),
    HumanMessage(
        content="""CONTEXT:
<NOTHING/>

INFO:
Please remember this: My favorite band is DragonForce
"""
    ),
    AIMessage(
        content=f"""<QA>
Q1: {Q1}
A1: YES

Q2: {Q2}
A2: YES

Q4: {Q3}
A3: YES
</QA>"""
    ),
]

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), *few_shot_examples, ("human", HUMAN_PROMPT)]
)

# LLM
llm = ChatCohere(model="command", temperature=0.5)


def parse_output(ai_message: str) -> bool:
    content: str = ai_message
    print("confirm_memorize: CONTENT START")
    print(content)

    a1: str = content[content.rindex("A1: ") + 4 :]
    a2: str = content[content.rindex("A2: ") + 4 :]
    a3: str = content[content.rindex("A3: ") + 4 :]

    a: List[str] = [a1, a2, a3]

    for an in a:
        if an.startswith("YES"):
            return True

    return False


retriever_embedder_type: ModelType = ModelType.HUGGINGFACE  # For now
# summarizer = convo_summarizer.chain


def format_inputs_for_retriever(inputs: Dict[str, Any]):
    global retriever_embedder_type

    community_id: int = inputs.pop("community_id")

    if len(inputs["context"]) == 0:
        inputs["context"] = "<NOTHING/>"

    # Goals
    retriever_prompt: str = PromptTemplate.from_template(HUMAN_PROMPT).format(**inputs)
    retriever = states.make_retriever(
        community_id, embedder_type=retriever_embedder_type
    )

    return RunnableLambda(lambda x: retriever_prompt) | retriever


# Create the chain
"""
Required inputs:
    {
        "context": str,  # the summarized context
        "info": str,
        "community_id": int
    }
"""
chain = (
    RunnableParallel(
        {
            "retrieved_context": RunnableLambda(format_inputs_for_retriever)
            | RunnableLambda(RAGQAChat.format_docs),
            # inputs
            "context": RunnableLambda(lambda d: d["context"]),
            "info": RunnableLambda(lambda d: d["info"]),
        }
    )
    | prompt
    | llm
    | StrOutputParser()
    | parse_output
)
