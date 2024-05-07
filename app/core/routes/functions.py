from typing import Union, Optional, List, Dict
from fastapi import APIRouter

import sqlalchemy
from app.core.db import database as db

from app.core.schemas.info import Lore, Belonging


router = APIRouter()


@router.post("/addlore")
async def put_lore(lore: Lore):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO lore(lore_text, about_chunk) VALUES (:lore_text, :about_chunk)",
                [lore.dict()],
            )
        )


@router.post("/addbelongings")
async def put_belongings(belongings: List[Belonging]):
    with db.engine.begin() as conn:
        vals: str = "(:content, :owner), " * len(belongings)
        vals = vals[:-2]

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO belongings(content, owner) VALUES {vals}",
                [belonging.dict() for belonging in belongings],
            )
        )
