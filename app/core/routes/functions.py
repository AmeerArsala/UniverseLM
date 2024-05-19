from typing import Union, Optional, List, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.schemas.info import Lore, Belonging
from app.lib import society


router = APIRouter()


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
