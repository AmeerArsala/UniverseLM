from typing import Union, Optional, List, Dict
from fastapi import APIRouter
from pydantic import BaseModel, Field

import sqlalchemy
from app.core.db import database as db

from app.core.schemas.entities import Chunk
from app.core.schemas.communities import Community

from app.lib import society


router = APIRouter()


@router.get("/communities")
async def get_communities() -> List[Community]:
    with db.engine.begin() as conn:
        results = conn.execute(sqlalchemy.text("SELECT * FROM communities")).fetchall()

        communities: List[Community] = [
            Community(id=id_, name=name) for (id_, name) in results
        ]

    return communities


@router.get("/community/{community_id}/entities")
async def get_chunks(community_id: int) -> List[Dict]:
    # TODO: do this

    return "TODO"


# TODO: do viewing of lore
# SELECT * FROM lore
# SELECT * FROM lore WHERE linked to chunks X, Y, and Z
