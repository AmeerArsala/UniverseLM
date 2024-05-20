from typing import Union, Optional, List, Dict, Tuple, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

import sqlalchemy
from app.core.db import database as db

from app.core.schemas.communities import Community
from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore, Belonging

from app.lib import society

from app.lib.utils.logic import LogicMode


router = APIRouter()


@router.get("/community/id/{name}")
async def get_community_id(name: str) -> int:
    with db.engine.begin() as conn:
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            [{"name": name}],
        ).first()

    return community_id


@router.get("/communities")
async def get_communities() -> List[Community]:
    with db.engine.begin() as conn:
        results: List[Tuple] = conn.execute(
            sqlalchemy.text("SELECT * FROM communities")
        ).fetchall()

        communities: List[Community] = [
            Community(id=id_, name=name) for (id_, name) in results
        ]

    return communities


@router.get("/community/{community_id}/chunks")
async def get_chunks(community_id: int) -> List[Chunk]:
    chunk_id_to_name: Dict[int, str] = {}

    with db.engine.begin() as conn:
        results: List[Tuple] = conn.execute(
            sqlalchemy.text("SELECT * FROM chunks WHERE community_id = :community_id"),
            [{"community_id": community_id}],
        ).fetchall()

        def record_chunk_dict(
            id_: int, name: str, profile: str, community_id_: int, parent_chunk: int
        ) -> Dict:
            chunk_id_to_name[id_] = name

            return {
                "id": id_,
                "name": name,
                "profile": profile,
                "community_id": community_id_,
                "parent_chunk": parent_chunk,  # these are just the ids
            }

        result_dicts: List[Dict] = [
            record_chunk_dict(id_, name, profile, community_id_, parent_chunk)
            for (id_, name, profile, community_id_, parent_chunk) in results
        ]

    def to_chunk(chunk_dict: Dict) -> Chunk:
        chunk_dict["parent_chunk"] = chunk_id_to_name[chunk_dict["parent_chunk"]]

        return Chunk(**chunk_dict)

    chunks: List[Chunk] = [to_chunk(chunk_dict) for chunk_dict in result_dicts]

    return chunks


class ViewLoreParams(BaseModel):
    involved_chunk_names: List[str] = Field(default=[])
    involved_chunks_logic: Any = Field(default="OR")
    return_involved_chunks: bool = Field(default=False)


@router.post("/community/{community_id}/lore")
async def view_lore(
    community_id: int, params: ViewLoreParams = ViewLoreParams()
) -> List[Lore]:
    """
    Viewing of lore
    SELECT * FROM lore
    SELECT * FROM lore WHERE linked to chunks X, Y, and/or/xor Z
    """
    # First, fix the params
    params.involved_chunks_logic = LogicMode.parse_str(params.involved_chunks_logic)

    # Now, do the lore view
    lore_views: List[Lore] = society.view_lore(community_id, **params.dict())

    return lore_views


class GetBelongingsParams(BaseModel):
    """Assumes existing knowledge of community_id"""

    owner_name: str = Field(default="")
    return_owner_name: bool = Field(
        default=False
    )  # can't ever be true if owner_name is specified


@router.post("/community/{community_id}/belongings")
async def get_belongings(
    community_id: int, params: GetBelongingsParams = GetBelongingsParams()
) -> List[Dict]:
    """
    3 possibilities:
        1 (default) - Return all belongings content, no owners:
                owner_name = ""
                return_owner_name = False
        2 - Return single belongings content, no owners (because it is already known by the fact it has to be passed in):
                owner_name = <str>
                return_owner_name = False
        3 - Return all belongings content, yes owners:
                owner_name = ""
                return_owner_name = True
    """
    owner_specified: bool = len(params.owner_name) > 0

    with db.engine.begin() as conn:
        other_fields: str = ", chunks.name" if params.return_owner_name else ""

        query: str = f"""
        SELECT content{other_fields}
        FROM belongings
        INNER JOIN chunks ON belongings.owner = chunks.id
        WHERE chunks.community_id = :community_id
        """

        query_vars: Dict = {"community_id": community_id}

        if owner_specified:
            query += " AND chunks.name = :owner_name"
            query_vars["owner_name"] = params.owner_name

        results: List[Tuple] = conn.execute(
            sqlalchemy.text(query), [query_vars]
        ).fetchall()

    belongings: List[Dict] = {}
    for result in results:
        belonging: Dict = {"content": result[0]}

        if params.return_owner_name:
            # means that there's another entry
            belonging["owner"] = result[1]

        belongings.append(belonging)

    return belongings
