from typing import Union, Optional, List, Dict
from fastapi import APIRouter

from app.core.schemas.info import Lore, Belonging
from app.lib import society


router = APIRouter()


@router.post("/addlore")
async def put_lore(lore: Lore):
    society.upload_lore([lore])

    return "OK"


@router.post("/addbelongings")
async def put_belongings(belongings: List[Belonging], owner: str, community_id: int):
    society.upload_belongings(belongings, owner, community_id)

    return "OK"


# TODO:
@router.post("/reset")
async def reset(community_id: int):
    society.reset(community_id)

    return "OK"
