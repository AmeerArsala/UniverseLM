from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

import app.core.db.database as db
import sqlalchemy

from app.lib import states
from app.lib.states import RawInfo

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore, Belonging

from app.lib.llm.prompts import chunk_summarizer

import numpy as np
import pandas as pd



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
def update(community_id: int):
    """Update the society by a tick"""
    
    return 0


# later, make a route that calls this
# the `count` parameter is ignored if `chunk_descs` is specified
def generate_chunks(chunk_descs: List[str] = [], desc: str = "", count: int = -1) -> List[Chunk]:
    """Agent Generation (for the lazy)"""
    chunks: List[Chunk] = []
    
    MIN_DESC_LENGTH = 3  # minimum length of word that we care about is 3
    
    has_community_desc: bool = len(desc) > MIN_DESC_LENGTH

    if len(chunk_descs) > 0:
        # Generate a description of the community if not already
        if not has_community_desc:
            # Generate from the chunk descs
            # Wow, this is lowkey an inherent form of prompt tuning
            # TODO:
            pass
        
        # From the community desc and chunk_descs, generate descriptions for each chunk
        # TODO:
    else:
        if count == -1:
            # Calculate a count
            MEAN_COUNT = 10
            MAX_DIFF = 5
            
            sign: int = int(np.sign(np.random.randn()))
            diff: int = sign * int(np.random.rand() * (MAX_DIFF + 1))

            count = MEAN_COUNT + diff
        
        if not has_community_desc:
            # Generate from nothing
            # TODO:
            pass
        
        # Now we have a count and community desc
        # Generate descriptions for each chunk given these
        # TODO:

    pass


# "Summary Statistics"
async def summarize_chunk(community_id: int, chunk_name: str) -> str:
    """
    Summarize findings (lore + belongings + profiles) about a chunk into a string. This can be used to profile a chunk
    """
    info: RawInfo = RawInfo()

    def add_to_info(profile_text: str, lore_text: str = "", belongings_text: str = ""):
        info.profiles_texts.append(profile_text)
        
        # if lore text exists
        if len(lore_text) > 0:
            info.lore_texts.append(lore_text)

        # if belongings text exists
        if len(belongings_text) > 0:
            info.belongings_texts.append(belongings_text)


    affiliation: str = ""
    
    # Steps:
    # 1. get all findings about the chunk from DB
    # 2. create a summarizer.py prompt 
    # 3. run it through
    with db.engine.begin() as conn:
        query = """
            SELECT chunks.profile, lore.lore_text, belongings.content
            FROM chunks
            INNER JOIN chunks_lore ON chunks.id = chunks_lore.chunk_id
            INNER JOIN lore ON chunks_lore.lore_id = lore.id
            INNER JOIN belongings ON chunks.id = belongings.owner
            WHERE chunks.community_id = :community_id AND chunks.name = :name
        """

        results = conn.execute(sqlalchemy.text(query, community_id=community_id, name=chunk_name)).fetchall()
        
        for result in results:
            add_to_info(*result)

        # Get affiliation now
        query = """
            SELECT c2.name
            FROM chunks c1 INNER JOIN chunks c2 ON c1.parent_chunk = c2.id
            WHERE c1.community_id = :community_id AND c1.name = :name
        """
        
        result = conn.execute(sqlalchemy.text(query, community_id=community_id, name=chunk_name)).first()
        
        (affiliation,) = result
        
    # Clean the duplicates out
    info.profiles_texts = pd.unique(info.profiles_texts).tolist()
    info.lore_texts = pd.unique(info.lore_texts).tolist()
    info.belongings_texts = pd.unique(info.belongings_texts).tolist()
    
    # Run the summarizer prompt
    summary: str = chunk_summarizer.chain.invoke(
            profile=info.profiles_texts[0],
            lore=info.lore_texts,
            belongings=info.belongings_texts,
            affiliation=affiliation
    )
    
    return summary

    
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

def reset(community_id: int):
    """Reset everything in the community"""
    # Clear the stuff in memory
    states.reset_state()

    # Now clear the whole database of the communities
    with db.engine.begin() as conn:
        # Delete the lore first
        query = """
        DELETE FROM lore
        WHERE EXISTS (
            SELECT 1 FROM chunks_lore
            JOIN chunks ON chunks_lore.chunk_id = chunks.id
            WHERE chunks_lore.lore_id = lore.id AND chunks.community_id = :community_id
        )
        """
        
        query2 = """
        DELETE FROM chunks_lore
        WHERE chunks_id IN (SELECT id FROM chunks WHERE chunks.community_id = :community_id)
        """

        query3 = """
        DELETE FROM belongings
        USING chunks
        WHERE belongings.owner = chunks.id AND chunks.community_id = :community_id
        """

        query4 = """
        DELETE FROM chunks
        WHERE community_id = :community_id
        """

        queries: List[str] = [query, query2, query3, query4]

        for query in queries:
            conn.execute(sqlalchemy.text(query, community_id=community_id))
        
        
    return "OK"
