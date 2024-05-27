from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core import api_auth

from app.core.schemas.entities import Chunk

from app.lib import society, states


router = APIRouter(tags=["apotheosis"], dependencies=[Depends(api_auth.get_api_key)])


class CreateCommunityParams(BaseModel):
    name: str


@router.post("/community")
async def create_community(params: CreateCommunityParams) -> int:
    community_id: int = society.create_community(params.name)

    return community_id


class CreateChunksParams(BaseModel):
    chunks: List[Chunk]


@router.post("/chunks")
async def create_chunks(params: CreateChunksParams):
    society.create_chunks(params.chunks)

    return "OK"


class CreateUserParams(BaseModel):
    email: str


@router.post("/user")
async def create_user(params: CreateUserParams) -> int:
    user_id: int = society.create_user(params.email)

    return user_id


class JoinCommunityParams(BaseModel):
    community_name: str
    user_email: str


@router.post("/community/join")
async def join_community(params: JoinCommunityParams):
    society.join_community(
        user_email=params.user_email, community_name=params.community_name
    )

    return "OK"
