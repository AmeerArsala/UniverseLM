from typing import List, Dict, Tuple

from langchain.prompts import ChatPromptTemplate
from langchain.llms import HuggingFaceHub
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

from app.core.schemas.entities import Chunk
import json

from langchain_google_genai import ChatGoogleGenerativeAI


# COMMUNITY DESC GENERATION CHAIN
# (count) -> community_desc: str

# TODO: GPT-orchestration (p-tuning) + few-shot this
community_system_prompt_message = """
Your role is to describe what a society is like including the individuals, groups, groups of groups, etc. that inhabit it. You are to IMAGINE this society. Given a specified number of entities (which refer to individuals, groups of individuals, groups of groups, etc.), you must generate an accurate all-encompassing big-picture description of said society. Be creative here but try to be accurate, as a small number of entities should not be in a society described for its vastness.
"""[
    1:-1
]

COMMUNITY_DESC_HUMAN_PROMPT = """
NUM ENTITIES: {num_entities}
"""

community_desc_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", community_system_prompt_message),
        ("human", COMMUNITY_DESC_HUMAN_PROMPT),
    ]
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
community_desc_chain = community_desc_prompt | community_desc_llm


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

gaslighting: List = [
    (
        "human",
        """COMMUNITY DESCRIPTION:
         A fantastical kingdom

NUMBER OF ENTITIES: 9""",
    ),
    AIMessage(
        content="""[
{
"Name": "King Arthur",
"Description": "The benevolent ruler of the kingdom, renowned for his wisdom and courage. His rule is marked by justice and prosperity.",
"Affiliation": "NONE"
},
{
"Name": "The Knights of the Round Table",
"Description": "A group of noble knights who serve under King Arthur. They are known for their chivalry, honor, and bravery in defending the kingdom.",
"Affiliation": "King Arthur"
},
{
"Name": "Merlin the Wizard",
"Description": "A powerful and wise wizard who serves as King Arthur's trusted advisor. His magical abilities have helped the kingdom in countless ways.",
"Affiliation": "King Arthur"
},
{
"Name": "Guinevere",
"Description": "The beautiful and kind-hearted queen of the kingdom. She is loved by all for her grace and compassion.",
"Affiliation": "King Arthur"
},
{
"Name": "The Enchanted Forest",
"Description": "A mystical forest filled with magical creatures and ancient secrets. It is a place of wonder and danger, often serving as a backdrop for adventures.",
"Affiliation": "NONE"
},
{
"Name": "The Dragon's Lair",
"Description": "A treacherous cavern deep within the mountains, home to a fearsome dragon. Legends say that great treasures lie within, guarded by the beast.",
"Affiliation": "NONE"
},
{
"Name": "The Elven Community",
"Description": "A secluded and peaceful community of elves, known for their grace, wisdom, and connection to nature. They occasionally assist the kingdom in times of need.",
"Affiliation": "NONE"
},
{
"Name": "The Dark Wizard's Tower",
"Description": "A foreboding tower located in the heart of the kingdom, where a malevolent dark wizard plots against the kingdom. His powers pose a constant threat to the realm.",
"Affiliation": "NONE"
},
{
"Name": "The Village of Camelot",
"Description": "The bustling capital of the kingdom, where people from all walks of life gather. It is a hub of trade, culture, and celebration, and the heart of King Arthur's rule.",
"Affiliation": "King Arthur"
}
]""",
    ),
    (
        "human",
        """COMMUNITY DESCRIPTION:
 A group of friends

NUMBER OF ENTITIES: 5""",
    ),
    AIMessage(
        content="""[
{
"Name": "Alex",
"Description": "A charismatic and outgoing individual who always brings laughter and positivity to the group. They are the life of the party and an excellent listener.",
"Affiliation": "NONE"
},
{
"Name": "Emily",
"Description": "A compassionate and empathetic person who is always there to support her friends. She has a passion for art and often shares her creations with the group.",
"Affiliation": "NONE"
},
{
"Name": "Michael",
"Description": "A reserved yet intellectual individual who enjoys deep conversations and debates. He is always eager to learn new things and share his knowledge with others.",
"Affiliation": "NONE"
},
{
"Name": "Olivia",
"Description": "An adventurous and spontaneous person who loves trying new experiences. She often organizes group outings and encourages everyone to step out of their comfort zones.",
"Affiliation": "NONE"
},
{
"Name": "The Book Club",
"Description": "A small group within the larger friend group, consisting of avid readers who share their thoughts and insights on various books. They meet regularly to discuss their latest reads and recommend new titles to one another.",
"Affiliation": "NONE"
}
]""",
    ),
    (
        "human",
        """COMMUNITY DESCRIPTION:
 A military academy

NUMBER OF ENTITIES: 7""",
    ),
    AIMessage(
        content="""[
{
"Name": "General Jackson",
"Description": "The stern and disciplined head of the academy, known for his unwavering dedication to training the next generation of military leaders. He commands respect and inspires excellence.",
"Affiliation": "NONE"
},
{
"Name": "Cadet Squad A",
"Description": "A group of highly motivated and skilled cadets who excel in physical training and tactical operations. They are often chosen for high-profile missions and assignments.",
"Affiliation": "General Jackson"
},
{
"Name": "Cadet Squad B",
"Description": "A group of cadets who specialize in strategy and intelligence gathering. They are known for their analytical skills and ability to think outside the box.",
"Affiliation": "General Jackson"
},
{
"Name": "Dr. Smith",
"Description": "A brilliant and innovative scientist who works closely with the academy to develop cutting-edge military technology. Her inventions have revolutionized the field of warfare.",
"Affiliation": "NONE"
},
{
"Name": "The Mess Hall",
"Description": "The bustling hub where cadets gather to eat, socialize, and occasionally engage in friendly competitions. It serves as a place for camaraderie and relaxation amidst the rigorous training.",
"Affiliation": "NONE"
},
{
"Name": "The War Games Arena",
"Description": "A sprawling outdoor facility where cadets participate in simulated combat exercises and strategic war games. It is a crucial part of their training and preparation for real-world missions.",
"Affiliation": "NONE"
},
{
"Name": "The Veterans' Association",
"Description": "A group of former cadets who have graduated from the academy and now serve in various branches of the military. They often return to mentor and guide current cadets, providing valuable insight and experience.",
"Affiliation": "NONE"
}
]""",
    ),
    (
        "human",
        """COMMUNITY DESCRIPTION:
A group of gangsters

NUMBER OF ENTITIES: 5""",
    ),
    AIMessage(
        content="""[
{
"Name": "Don Vito",
"Description": "The cunning and ruthless leader of the gang, known for his sharp intellect and brutal tactics. He commands respect and fear among his underlings.",
"Affiliation": "NONE"
},
{
"Name": "The Enforcers",
"Description": "A group of fiercely loyal and lethal gang members who serve as Don Vito's personal bodyguards and muscle. They are known for their unwavering loyalty and willingness to carry out any order without question.",
"Affiliation": "Don Vito"
},
{
"Name": "The Smugglers",
"Description": "A group of skilled and resourceful gang members who specialize in trafficking illegal goods and contraband. They are known for their ability to navigate complex networks and evade law enforcement.",
"Affiliation": "Don Vito"
},
{
"Name": "The Informant",
"Description": "A mysterious and elusive figure who provides valuable information to the gang in exchange for protection and favors. Their identity remains unknown, but their intel is invaluable to the gang's operations.",
"Affiliation": "NONE"
},
{
"Name": "The Hideout",
"Description": "A secret and heavily fortified location where the gang gathers to plan their operations and lay low from authorities. It is a place of refuge and strategy, where the gang members can regroup and strategize.",
"Affiliation": "NONE"
}
]""",
    ),
    (
        "human",
        """COMMUNITY DESCRIPTION:
A rich family of 5 that is currently facing a scandal

NUMBER OF ENTITIES: 5""",
    ),
    AIMessage(
        content="""[
{
"Name": "Patriarch Robert",
"Description": "The respected and influential head of the family, known for his business acumen and philanthropic endeavors. He is now embroiled in a scandal that threatens to tarnish his reputation and legacy.",
"Affiliation": "NONE"
},
{
"Name": "Matriarch Elizabeth",
"Description": "The elegant and graceful matriarch of the family, renowned for her charitable work and social connections. She stands by her husband amidst the scandal, working tirelessly to protect their family's image.",
"Affiliation": "Patriarch Robert"
},
{
"Name": "Heir Apparent William",
"Description": "The ambitious and driven heir to the family fortune, eager to prove himself amidst the scandal. He works closely with his parents to navigate the crisis and secure the family's future.",
"Affiliation": "Patriarch Robert"
},
{
"Name": "Socialite Charlotte",
"Description": "The glamorous and outspoken daughter of the family, known for her lavish lifestyle and high-profile relationships. She finds herself in the spotlight during the scandal, causing further complications for the family.",
"Affiliation": "Patriarch Robert"
},
{
"Name": "The Family Lawyers",
"Description": "A team of skilled and discreet attorneys who handle the family's legal affairs. They work around the clock to mitigate the damage caused by the scandal and protect the family's interests.",
"Affiliation": "Patriarch Robert"
}
]""",
    ),
]

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt_message), *gaslighting, ("human", HUMAN_PROMPT)]
)

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro")


def parse_chunks(ai_message: str, community_id: int) -> List[Chunk]:
    chunks: List[Chunk] = []

    output: str = ai_message  # ai_message[ai_message.rindex("AI: ") + 4 :]
    print("OUTPUT START")
    print(output)

    # Given the output of the llm and a `community_id`, parse into a List[Chunk]
    chunk_dicts: List[Dict] = json.loads(output)

    # TODO: The LLM must be gaslighted into returning a list of dicts as described below
    chunks = [
        Chunk(
            name=chunk_dict["Name"],
            profile=chunk_dict["Description"],
            community_id=community_id,
            parent_chunk=chunk_dict["Affiliation"],
        )
        for chunk_dict in chunk_dicts
    ]

    return chunks


def dynamic_route(info: Dict):
    inputs: Dict[str, str] = {
        "num_chunks": lambda args: info["num_chunks"],
        "community_desc": lambda args: info["community_desc"],
    }

    def parse_output(ai_message: AIMessage) -> List[Chunk]:
        community_id: int = info["community_id"]

        return parse_chunks(ai_message, community_id)

    return inputs | prompt | llm | StrOutputParser() | parse_output


# Create the chain
chain = RunnableParallel(
    {
        "num_chunks": RunnablePassthrough(),
        "community_desc": RunnablePassthrough(),
        "community_id": RunnablePassthrough(),
    }
) | RunnableLambda(dynamic_route)
