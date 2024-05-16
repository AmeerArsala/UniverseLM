from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

import app.core.db.database as db
import sqlalchemy

from langchain_core.documents import Document

from app.lib.llm.rag import ModelType, create_retriever


# Search across the whole thing for retrieval
class RawInfo(BaseModel):
    # re-pull (async) on update (upload_lore)
    lore_texts: List[str] = Field(default=[])

    # re-pull (async) on update (upload_belongings)
    belongings_texts: List[str] = Field(default=[])

    # re-pull (async) on update (set_profile)
    profiles_texts: List[str] = Field(default=[])

    def to_docs(self, return_strs: bool = False) -> List:
        all_texts: List[str] = (
            self.profiles_texts + self.lore_texts + self.belongings_texts
        )

        if return_strs:
            return all_texts

        return [Document(page_content=text) for text in all_texts]


# GameState
known_chunks: Dict[int, List[str]] = {}  # known chunk names for LLMs to keep track of
community_states: Dict[int, RawInfo] = {}


def reset_state():
    global known_chunks, community_states

    known_chunks = {}
    community_states = {}


async def startup(community_id: int):
    global known_chunks, community_states

    # known_chunks
    await refresh_known_chunks(community_id)

    # community_states
    await pull_lore(community_id)
    await pull_belongings(community_id)
    await pull_profiles(community_id)

    print("Community startup complete.")


def make_retriever(community_id: int, embedder_type: ModelType):
    global community_states

    docs: List[Document] = community_states[community_id].to_docs()

    return create_retriever(embedder_type, docs)


async def refresh_all_known_chunks() -> Dict[int, List[str]]:
    global known_chunks

    with db.engine.begin() as conn:
        results = conn.execute(
            sqlalchemy.text("SELECT community_id, name FROM chunks")
        ).fetchall()

        all_known_chunks: Dict[int, List[str]] = {}
        for result in results:
            (community_id, name) = result

            if all_known_chunks.get(community_id) is None:
                all_known_chunks[community_id] = []

            all_known_chunks[community_id].append(name)

    known_chunks = all_known_chunks

    return known_chunks


async def refresh_known_chunks(community_id: int) -> List[str]:
    global known_chunks

    with db.engine.begin() as conn:
        results = conn.execute(
            sqlalchemy.text("SELECT name FROM chunks WHERE community_id = :id"),
            [dict(id=community_id)],
        ).fetchall()

        chunk_names: List[str] = [result[0] for result in results]

    known_chunks[community_id] = chunk_names

    return known_chunks[community_id]


def set_infostate(community_id: int, **vals):
    global community_states

    if community_states.get(community_id) is None:
        community_states[community_id] = RawInfo()

    for key, val in vals.items():
        setattr(community_states[community_id], key, val)


async def pull_lore(community_id: int):
    global community_states

    with db.engine.begin() as conn:
        query = """
            SELECT lore_text
            FROM lore
            INNER JOIN chunks_lore ON lore.id = chunks_lore.lore_id
            INNER JOIN chunks ON chunks_lore.chunk_id = chunks.id
            WHERE chunks.community_id = :community_id
        """

        results = conn.execute(
            sqlalchemy.text(query), [dict(community_id=community_id)]
        ).fetchall()

        lore_texts: List[str] = [result[0] for result in results]

        set_infostate(community_id, lore_texts=lore_texts)


async def pull_belongings(community_id: int):
    global community_states

    with db.engine.begin() as conn:
        query = """
            SELECT content
            FROM belongings
            INNER JOIN chunks ON belongings.owner = chunks.id
            WHERE chunks.community_id = :community_id
        """

        results = conn.execute(
            sqlalchemy.text(query), [dict(community_id=community_id)]
        ).fetchall()

        belongings_texts: List[str] = [result[0] for result in results]
        set_infostate(community_id, belongings_texts=belongings_texts)


async def pull_profiles(community_id: int):
    global community_states

    with db.engine.begin() as conn:
        query = """
            SELECT name, profile
            FROM chunks
            WHERE community_id = :community_id
        """

        results = conn.execute(
            sqlalchemy.text(query), [dict(community_id=community_id)]
        ).fetchall()

        profiles_texts: List[str] = [f"{result[0]} - {result[1]}" for result in results]
        set_infostate(community_id, profiles_texts=profiles_texts)
