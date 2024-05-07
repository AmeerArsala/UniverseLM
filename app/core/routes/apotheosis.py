from typing import Union, Optional, List, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

import sqlalchemy
from app.core.db import database as db

from app.core.schemas.entities import User, Chunk


router = APIRouter()


@router.post("/community")
async def create_community(name: str):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO communities(name) VALUES (:commmunity_name)",
                [{"community_name": name}],
            )
        )


@router.post("/chunks")
async def create_chunks(chunks: List[Chunk]):
    with db.engine.begin() as conn:
        vals: str = "(:name, :profile, :community_id, :parent_chunk), " * len(chunks)
        vals = vals[:-2]

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO chunks(name, profile, community_id, parent_chunk) VALUES {vals}",
                [chunk.dict() for chunk in chunks],
            )
        )


@router.post("/user")
async def create_user(user: User):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO users(email, chunk_name) VALUES (:email, :chunk_name)",
                [user.dict()],
            )
        )
