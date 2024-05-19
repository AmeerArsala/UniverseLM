# Extract information to memorize in lore
from typing import List, Dict
from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel


# Prompting
# TODO: GPT-orchestration (p-tuning) + few-shot this
system_prompt_message = """
# Instruction
You are a recordkeeper who records important information. Your role is to extract the relevant and most important information (from the new information) about the given conversation and rephrase it in your response as well as mention which entities are involved with this information.
Given a list of all possible named entities, the context of the conversation, and the new information (typically the most recent piece of dialogue in the conversation), you are to extract the most important key information from the given new information and rephrase it in your response as if it were 'lore' in a story.

In general, you should be considering information important if:
A) The new information might command/instruct you to memorize/remember something, in which case your response should contain the stuff they want you to remember as 'lore'
B) The information given the context is actually a key piece of information (and not just filler) that is genuinely important to the matter at hand. If this were a fictional world, the important information would essentially be important lore or new events that occur.
C) If the new information starts referring to entities that are on the list of all possible named entities, then chances are that it is important, because a big purpose of this task is to record lore about said named entities

Make sure to utilize the context of the conversation to help inform your response (such as deciding which piece of information is the most important).

Additionally, you must mention which named entities are involved within the new info. Separate them by new lines, just like the list of "ALL POSSIBLE NAMED ENTITIES". Also just like that list, when referring to a named entity, you must use the same exact spelling and case as the list of all possible named entities.

# Constraint
- Speak declaratively/objectively and in 3rd person as if this is recorded lore. Do not treat your response like a conversational reply
- You MUST address any referred to entity/proper noun (person, place, or thing) DIRECTLY and in 3rd person. For example, you cannot refer to anyone by their pronouns even if the given information says it; you must instead use their actual name, which you can use the context and list of all possible named entities to determine. This applies to both the "EXTRACTED IMPORTANT NEW INFO" and "NAMED ENTITIES INVOLVED"
- When returning the "NAMED ENTITIES INVOLVED", refer to entities exactly as they are referred to in "ALL POSSIBLE NAMED ENTITIES" (same spelling, case, etc.); their actual name. As described before, separate by new lines.
"""[
    1:-1
]

HUMAN_PROMPT = """
ALL POSSIBLE NAMED ENTITIES:
{all_entities}

CONTEXT:
{context}

NEW INFO:
{info}

"""[
    1:
]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_message),
        (
            "human",
            """ALL POSSIBLE NAMED ENTITIES:
King Arthur
The Knights of the Round Table
Merlin the Wizard
Guinevere
The Enchanted Forest
The Dragon's Lair
The Elven Community
The Dark Wizard's Tower
The Village of Camelot

CONTEXT:
N/A

NEW INFO:
King Arthur - I'm searching the Enchanted Forest in order to meet up with the Elven Community so they can heal me up after my fierce battle with the Dark Wizard in his tower. 

""",
        ),
        (
            "ai",
            """EXTRACTED IMPORTANT NEW INFO:
After a fierce battle with the Dark Wizard in the Dark Wizard's Tower, King Arthur is currently in the Enchanted Forest searching for The Elven Community so they can heal him.

NAMED ENTITIES INVOLVED:
King Arthur
The Enchanted Forest
The Dark Wizard's Tower""",
        ),
        ("human", HUMAN_PROMPT),
    ]
)


def parse_output(content: str) -> Dict:
    output_dict: Dict = {}

    EXTRACTED_IMPORTANT_INF_TOKEN = "NEW INFO:\n"
    NAMED_ENTS_TOKEN = "NAMED ENTITIES INVOLVED:\n"

    extracted_info_idx: int = content.rindex(EXTRACTED_IMPORTANT_INF_TOKEN)
    named_entities_idx: int = content.rindex(NAMED_ENTS_TOKEN)

    output_content: str = content[
        extracted_info_idx + len(EXTRACTED_IMPORTANT_INF_TOKEN) : named_entities_idx
    ].strip()
    named_entities_str: str = content[named_entities_idx + len(NAMED_ENTS_TOKEN) :]

    named_entities: List[str] = named_entities_str.split("\n")

    while len(named_entities[-1]) == 0:
        named_entities.pop(-1)  # remove the last one

    output_dict["extracted_info"] = output_content
    output_dict["about_entities"] = named_entities

    print(f"extract_lore: {output_dict}")

    return output_dict


# LLM
LLM_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
    repo_id=LLM_ID, model_kwargs={"temperature": 0.5, "max_length": 5000}
)


# Create the chain
extract_chain = prompt | llm | StrOutputParser() | parse_output


# def extract_entities_involved(
#     extracted_info: str, possible_entities: List[str]
# ) -> List[str]:
#     print("extract_lore: EXTRACTED INFO START")
#     print(extracted_info)
#
#     assert not extracted_info.startswith("System")
#
#     entities: List[str] = []
#
#     for entity in possible_entities:
#         if entity in extracted_info:
#             entities.append(entity)
#
#     return entities


# Create the overall chain
"""
Inputs:
    {
        "possible_entities": List[str],
        "context": str,  # the summarized context
        "info": str
    }

Outputs:
    {
        "extracted_info": str,
        "about_entities": List[str]
    }
"""
chain = (
    RunnableLambda(
        lambda d: {
            "all_entities": "\n".join(d["possible_entities"]),
            "context": d["context"] if len(d["context"]) > 0 else "N/A",
            "info": d["info"],
        }
    )
    | extract_chain
)
# chain = RunnableParallel(
#     {
#         "extracted_info": RunnableLambda(
#             lambda d: {
#                 "all_entities": "\n".join(d["possible_entities"]),
#                 "context": d["context"] if len(d["context"]) > 0 else "N/A",
#                 "info": d["info"],
#             }
#         )
#         | extract_chain,
#         "possible_entities": RunnableLambda(lambda d: d["possible_entities"]),
#     }
# ).assign(about_entities=(lambda d: extract_entities_involved(**d)))
