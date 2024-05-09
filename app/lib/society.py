from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

import app.core.db.database as db
import sqlalchemy

from app.lib import states

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore, Belonging


# CREATION
# --------


def create_community(name: str) -> int:
    with db.engine.begin() as conn:
        result: Tuple = conn.execute(
            sqlalchemy.text(
                "INSERT INTO communities(name) VALUES (:commmunity_name) RETURNING id",
                [{"community_name": name}],
            )
        ).first()

        id_: int = result[0]

    return id_


def create_chunks(chunks: List[Chunk]):
    with db.engine.begin() as conn:
        vals: str = "(:name, :profile, :community_id, :parent_chunk), " * len(chunks)
        vals = vals[:-2]

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO chunks(name, profile, community_id, parent_chunk) VALUES {vals}",
                [chunk.dict() for chunk in chunks],
            )
        )


def create_user(email: str):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO users(email) VALUES (:email)",
                [{"email": email}],
            )
        )


def join_community(user_email: str, community_name: str):
    with db.engine.begin() as conn:
        # First get the user_id and community_id
        user_id: int = conn.execute(
            sqlalchemy.text(
                "SELECT id FROM users WHERE email = :email", [{"email": user_email}]
            )
        ).first()[0]

        community_id: int = conn.execute(
            sqlalchemy.text(
                "SELECT id FROM communities WHERE name = :name",
                [{"name": community_name}],
            )
        ).first()[0]

        # Now link the user and the community by inserting them into the junction table
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO users_communities(user_id, community_id) VALUES (:user_id, :community_id)",
                [{"user_id": user_id, "community_id": community_id}],
            )
        )


# --------

# UPDATES
# --------


# later, make a route that calls this
# This is the update method and the main driver of the society
def update():
    """Update the society by a tick"""
    pass


# make a route that calls this
def generate_chunks() -> List[Chunk]:
    """Agent Generation (for the lazy)"""
    pass


# "Summary Statistics"
async def summarize_chunk(chunk_name: str) -> str:
    """
    Summarize findings (lore + belongings + profiles) about a chunk into a string. This can be used to profile a chunk
    """
    pass


# Upload new lore to DB
async def upload_lore(lore: List[Lore], community_id: int):
    lore_count: int = len(lore)

    with db.engine.begin() as conn:
        # First, insert into lore and get the corresponding list of lore_ids
        vals: str = "(:lore_text), " * lore_count
        vals = vals[:-2]

        lore_text_vars = {f"lore_text{i}": lore_piece.lore_text for (i, lore_piece) in enumerate(lore)}
        
        results = conn.execute(
            sqlalchemy.text(
                f"INSERT INTO lore(lore_text) VALUES {",".join([f":{placeholder}" for placeholder in lore_text_vars.keys()])} RETURNING id",
                **lore_text_vars,
            )
        ).fetchall()

        lore_ids: List[int] = [result[0] for result in results]

        # Now, insert into chunks_lore
        query: str = "INSERT INTO chunks_lore(chunk_id, lore_id) VALUES "
        row_mappings: Dict[str, Tuple[int, int]] = {}
        
        n: int = 1
        for lore_piece, lore_id in zip(lore, lore_ids):
            num_about: int = len(lore_piece.about_chunks)

            # Get corresponding list of chunk_ids
            results = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT id FROM chunks 
                    WHERE community_id = :community_id AND name IN :names
                    """,
                    community_id=community_id, names=tuple(lore_piece.about_chunks),
                )
            ).fetchall()

            chunk_ids: List[int] = [result[0] for result in results]
            
            for (i, chunk_id) in enumerate(chunk_ids):
                placeholder: str = f"row{n+i}"
                row: Tuple[int, int] = (chunk_id, lore_id)
                
                # Put it in mappings
                row_mappings[placeholder] = row 

            n += num_about
        
        # Add in the placeholders to the query
        query += ",".join([f":{placeholder}" for placeholder in row_mappings.keys()])

        # Execute the bulk insertion
        conn.execute(sqlalchemy.text(query, **row_mappings))
    
    # Pull lore
    states.pull_lore(community_id)


# Upload new belongings to DB
async def upload_belongings(belongings: List[Belonging], owner: str, community_id: int):
    with db.engine.begin() as conn:
        # First, get corresponding owner_id
        owner_id: int = conn.execute(sqlalchemy.text("SELECT id FROM chunks WHERE community_id = :community_id AND name = :name", 
                                     community_id=community_id, name=owner)).first()[0]
        
        # Generate the tuple values
        rows: Dict[str, Tuple[str, int]] = {f"row{i}": (belonging.content, owner_id) for (i, belonging) in belongings}

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO belongings(content, owner) VALUES {",".join([f":{placeholder}" for placeholder in rows.keys()])}",
                **rows,
            )
        )
    
    # Pull belongings
    states.pull_belongings(community_id)


# Set profile
async def set_profile(community_id: int, chunk_name: str, content: str):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                UPDATE chunks
                SET profile = :profile
                WHERE community_id = :community_id AND chunk_name = :name
                """,
                [
                    {
                        "profile": content,
                        "name": chunk_name,
                        "community_id": community_id,
                    }
                ],
            )
        )
    
    # Pull profiles
    states.pull_profiles(community_id)


# --------
