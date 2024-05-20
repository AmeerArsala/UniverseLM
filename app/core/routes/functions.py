from typing import Union, Optional, List, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore, Belonging
from app.lib import society, states, users


router = APIRouter(prefix="/{community_id}")


@router.post("/startup")
async def startup_community(community_id: int):
    await states.startup(community_id=community_id)

    return "OK"


class InhabitChunkParams(BaseModel):
    user_id: int
    chunk_name: str


@router.post("/chunks/inhabit")
async def user_inhabit_chunk(community_id: int, params: InhabitChunkParams):
    users.inhabit_chunk(
        user_id=params.user_id, community_id=community_id, chunk_name=params.chunk_name
    )

    return "OK"


@router.get("/chunks/refresh")
async def refresh_known_chunks(community_id: int) -> List[str]:
    known_chunks_for_community: List[str] = states.refresh_known_chunks(community_id)

    return known_chunks_for_community


class GenerateChunksParams(BaseModel):
    chunk_descs: List[str] = Field(default=[])
    desc: str = Field(default="")
    count: int = Field(default=-1)


@router.post("/chunks/generate")
async def generate_chunks(
    community_id: int, params: GenerateChunksParams = GenerateChunksParams()
) -> List[Chunk]:
    generated_chunks: List[Chunk] = society.generate_chunks(
        community_id, **params.dict()
    )

    return generated_chunks


class PutLoreParams(BaseModel):
    lore: List[Lore]


@router.post("/add_lore")
async def put_lore(community_id: int, params: PutLoreParams):
    society.upload_lore(params.lore, community_id)

    return "OK"


class PutBelongingsParams(BaseModel):
    belongings: List[Belonging]
    owner: str


@router.post("/add_belongings")
async def put_belongings(community_id: int, params: PutBelongingsParams):
    society.upload_belongings(params.belongings, params.owner, community_id)

    return "OK"


@router.post("/reset")
async def reset(community_id: int):
    society.reset(community_id)

    return "OK"


@router.post("/update")
async def update(community_id: int):
    society.update(community_id)

    return "OK"
