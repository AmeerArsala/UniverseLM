from typing import List, Dict
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Request

from app.core import api_auth
from app.lib import society, states, users


router = APIRouter(tags=["admin"], dependencies=[Depends(api_auth.get_admin_api_key)])


@router.post("/refresh_all_chunks")
async def refresh_all_known_chunks() -> Dict[int, List[str]]:
    return states.refresh_all_known_chunks()


class CreateUserParams(BaseModel):
    email: str


@router.post("/create_user")
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
