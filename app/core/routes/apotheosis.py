from typing import Union, Optional, List, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

import sqlalchemy
from app.core.db import database as db

from app.core.schemas.entities import Chunk

from app.lib import society


router = APIRouter()


@router.post("/community")
async def create_community(name: str) -> int:
    community_id: int = society.create_community(name)

    return community_id


@router.post("/chunks")
async def create_chunks(chunks: List[Chunk]):
    society.create_chunks(chunks)


@router.post("/user")
async def create_user(email: str):
    society.create_user(email)
