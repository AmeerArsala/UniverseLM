from typing import Union, Optional, List, Dict
from pydantic import BaseModel, Field

from app.lib.chat import AgentChatParams


class ChunkInhabitance(BaseModel):
    community_id: int
    chunk_name: str


# user_id: int
inhabitances: Dict[int, ChunkInhabitance] = {}


# The User inhabits a chunk in order to talk to another chunk
def inhabit_chunk(user_id: int, community_id: int, chunk_name: str):
    global inhabitances

    inhabitances[user_id] = ChunkInhabitance(
        community_id=community_id, chunk_name=chunk_name
    )


def make_chat_input(user_id: int, message: str) -> AgentChatParams:
    global inhabitances

    inhabitance: ChunkInhabitance = inhabitances[user_id]

    return AgentChatParams(question=message, sender_chunk_name=inhabitance.chunk_name)
