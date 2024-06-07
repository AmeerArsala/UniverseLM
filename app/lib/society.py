from typing import Callable, List, Dict, Tuple, Set
from pydantic import BaseModel, Field

import app.core.db.database as db
import sqlalchemy

from app.lib import states
from app.lib.states import RawInfo

from app.core.schemas.entities import Chunk
from app.core.schemas.info import Lore, Belonging

from app.lib.llm.prompts import chunk_summarizer
from app.lib.llm.prompts.chunk_generation import (
    with_chunk_descs as chunk_generation_with_chunk_descs,
    without_chunk_descs as chunk_generation_without_chunk_descs,
)

from app.lib.utils.logic import LogicMode

import numpy as np
import pandas as pd


"""
HOW THE SIMULATION WORKS:

1. Create User
2. Create Community & Have User join community
3. From inside the community, a variety of things can happen:
    * First, Community must be locally started up (sync local)
    * Then, User MUST inhabit a Chunk before doing any action (such as talking to other chunks), but User can still view lore of community
    - User may view lore of everyone
    - User may create chunks and upload their own lore, belongings, and set profiles of chunks
    - Community global update tick
    - Chunks may be auto-generated via an overall community desc, a chunk count, and/or a list of rudimentary chunk descriptions
    - User may chat with other chunks and generate lore that is automatically updated and uploaded to a DB
    - Reset everything
"""


# CREATION
# --------


def create_community(name: str) -> int:
    with db.engine.begin() as conn:
        result: Tuple = conn.execute(
            sqlalchemy.text(
                "INSERT INTO communities(name) VALUES (:community_name) RETURNING id",
            ),
            [{"community_name": name}],
        ).first()

        id_: int = result[0]

    return id_


def create_chunks(chunks: List[Chunk]):
    with db.engine.begin() as conn:
        uploadable_dicts: List[Dict] = Chunk.as_uploadable_dicts(chunks)
        overall_upload_dict: Dict = {}
        vals: str = ""

        for i, chunk_dict in enumerate(uploadable_dicts):
            id_ = f"id{i}"
            name_ = f"name{i}"
            profile_ = f"profile{i}"
            community_id_ = f"community_id{i}"
            parent_chunk_ = f"parent_chunk{i}"

            # Modify the dict now
            chunk_dict[id_] = chunk_dict.pop("id")
            chunk_dict[name_] = chunk_dict.pop("name")
            chunk_dict[profile_] = chunk_dict.pop("profile")
            chunk_dict[community_id_] = chunk_dict.pop("community_id")
            chunk_dict[parent_chunk_] = chunk_dict.pop("parent_chunk")

            vals += (
                f"(:{id_}, :{name_}, :{profile_}, :{community_id_}, :{parent_chunk_}),"
            )

            overall_upload_dict.update(chunk_dict)
            print(chunk_dict)

        vals = vals[:-1]  # ignore last `,`

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO chunks(id, name, profile, community_id, parent_chunk) VALUES {vals}"
            ),
            [overall_upload_dict],
        )


def create_user(email: str) -> int:
    with db.engine.begin() as conn:
        result: Tuple = conn.execute(
            sqlalchemy.text("INSERT INTO users(email) VALUES (:email) RETURNING id"),
            [{"email": email}],
        ).first()

        id_: int = result[0]

    return id_


def join_community(user_email: str, community_name: str):
    with db.engine.begin() as conn:
        # First get the user_id and community_id
        user_id: int = conn.execute(
            sqlalchemy.text("SELECT id FROM users WHERE email = :email"),
            [{"email": user_email}],
        ).first()[0]

        community_id: int = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            [{"name": community_name}],
        ).first()[0]

        # Now link the user and the community by inserting them into the junction table
        conn.execute(
            sqlalchemy.text(
                "INSERT INTO users_communities(user_id, community_id) VALUES (:user_id, :community_id)"
            ),
            [{"user_id": user_id, "community_id": community_id}],
        )


# later, make a route that calls this
# the `count` parameter is ignored if `chunk_descs` is specified
def generate_chunks(
    community_id: int, chunk_descs: List[str] = [], desc: str = "", count: int = -1
) -> List[Chunk]:
    """Agent Generation (for the lazy)"""
    chunks: List[Chunk] = []
    lazy_chunk_descs: List[str] = chunk_descs.copy()

    MIN_DESC_LENGTH = 3  # minimum length of word that we care about is 3

    has_community_desc: bool = len(desc) > MIN_DESC_LENGTH

    if len(lazy_chunk_descs) > 0:
        # Generate a description of the community if not already
        if not has_community_desc:
            # Generate from the chunk descs
            # Wow, this is lowkey an inherent form of prompt tuning
            # (chunk_descs[]) -> community_desc: str
            desc = chunk_generation_with_chunk_descs.community_desc_chain.invoke(
                lazy_chunk_descs=lazy_chunk_descs
            )

        # From the community desc and chunk_descs, generate descriptions for each chunk
        # (lazy_chunk_descs[], community_desc) -> chunk_descs[str]
        X = 3
        while len(lazy_chunk_descs) > 0:
            # Pop out the first X items
            x = min(X, len(lazy_chunk_descs))
            selected_lazy_chunk_descs: List[str] = lazy_chunk_descs[:x]
            del lazy_chunk_descs[:x]

            # Postprocess into List[Chunk]
            generated_chunks: List[Chunk] = (
                chunk_generation_with_chunk_descs.chain.invoke(
                    dict(
                        lazy_chunk_descs=selected_lazy_chunk_descs,
                        community_desc=desc,
                        community_id=community_id,
                    )
                )
            )

            # Add them all to the list
            chunks += generated_chunks
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
            # (count) -> community_desc
            desc = chunk_generation_without_chunk_descs.community_desc_chain.invoke(
                dict(num_chunks=count)
            )

        # Now we have a count and community desc
        # Generate descriptions for each chunk given these
        # (count, community_desc) -> chunk_descs[str]
        chunks = chunk_generation_without_chunk_descs.chain.invoke(
            {"num_chunks": count, "community_desc": desc, "community_id": community_id}
        )

    return chunks


# --------

# UPDATES
# --------


# later, make a route that calls this
# This is the update method and the main driver of the society
def update(community_id: int):
    """Update the society by a tick"""

    return 0


# "Summary Statistics"
def summarize_chunk(community_id: int, chunk_name: str) -> str:
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

        results = conn.execute(
            sqlalchemy.text(query), [dict(community_id=community_id, name=chunk_name)]
        ).fetchall()

        for result in results:
            add_to_info(*result)

        # Get affiliation now
        query = """
            SELECT c2.name
            FROM chunks c1 INNER JOIN chunks c2 ON c1.parent_chunk = c2.id
            WHERE c1.community_id = :community_id AND c1.name = :name
        """

        result = conn.execute(
            sqlalchemy.text(query), [dict(community_id=community_id, name=chunk_name)]
        ).first()

        (affiliation,) = result

    # Clean the duplicates out
    info.profiles_texts = pd.unique(np.array(info.profiles_texts)).tolist()
    info.lore_texts = pd.unique(np.array(info.lore_texts)).tolist()
    info.belongings_texts = pd.unique(np.array(info.belongings_texts)).tolist()

    # Run the summarizer prompt
    summary: str = chunk_summarizer.chain.invoke(
        profile=info.profiles_texts[0],
        lore=info.lore_texts,
        belongings=info.belongings_texts,
        affiliation=affiliation,
    )

    return summary


# Upload new lore to DB
def upload_lore(lore: List[Lore], community_id: int):
    lore_count: int = len(lore)

    with db.engine.begin() as conn:
        # First, insert into lore and get the corresponding list of lore_ids
        vals: str = "(:lore_text), " * lore_count
        vals = vals[:-2]

        lore_text_vars = {
            f"lore_text{i}": str(lore_piece.lore_text)
            for (i, lore_piece) in enumerate(lore)
        }

        vals = ",".join([f"(:{placeholder})" for placeholder in lore_text_vars.keys()])

        results = conn.execute(
            sqlalchemy.text(f"INSERT INTO lore(lore_text) VALUES {vals} RETURNING id"),
            [lore_text_vars],
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
                    """
                ),
                [
                    {
                        "community_id": community_id,
                        "names": tuple(lore_piece.about_chunks),
                    }
                ],
            ).fetchall()

            chunk_ids: List[int] = [result[0] for result in results]

            for i, chunk_id in enumerate(chunk_ids):
                placeholder: str = f"row{n+i}"
                row: Tuple[int, int] = (chunk_id, lore_id)

                # Put it in mappings
                row_mappings[placeholder] = row

            n += num_about

        # Add in the placeholders to the query
        query += ",".join([f":{placeholder}" for placeholder in row_mappings.keys()])

        # Execute the bulk insertion
        conn.execute(sqlalchemy.text(query), [row_mappings])

    # Pull lore
    states.pull_lore(community_id)


# Upload new belongings to DB
def upload_belongings(belongings: List[Belonging], owner: str, community_id: int):
    with db.engine.begin() as conn:
        # First, get corresponding owner_id
        owner_id: int = conn.execute(
            sqlalchemy.text(
                "SELECT id FROM chunks WHERE community_id = :community_id AND name = :name"
            ),
            [{"community_id": community_id, "name": owner}],
        ).first()[0]

        # Generate the tuple values
        rows: Dict[str, Tuple[str, int]] = {
            f"row{i}": (belonging.content, owner_id) for (i, belonging) in belongings
        }

        values_str: str = ",".join([f":{placeholder}" for placeholder in rows.keys()])

        conn.execute(
            sqlalchemy.text(
                f"INSERT INTO belongings(content, owner) VALUES {values_str}"
            ),
            [rows],
        )

    # Pull belongings
    states.pull_belongings(community_id)


# Set profile
def set_profile(community_id: int, chunk_name: str, content: str):
    with db.engine.begin() as conn:
        conn.execute(
            sqlalchemy.text(
                """
                UPDATE chunks
                SET profile = :profile
                WHERE community_id = :community_id AND chunk_name = :name
                """
            ),
            [{"profile": content, "name": chunk_name, "community_id": community_id}],
        )

    # Pull profiles
    states.pull_profiles(community_id)


# --------

# REAP (view)
# --------


def retrieve_lore(
    community_id: int,
    involved_chunk_names: List[str] = [],
    return_involved_chunks: bool = False,
) -> List[Lore]:
    """View lore of the involved chunks. If not specified, then view all lore"""
    with db.engine.begin() as conn:
        other_fields: str = ""
        other_conditions: str = ""

        query_vars: Dict = {"community_id": community_id}

        def make_query():
            additional_conditions: str = (
                f" AND ({other_conditions})" if len(involved_chunk_names) > 0 else ""
            )

            return f"""
            SELECT DISTINCT lore.lore_text{other_fields} 
            FROM lore 
            INNER JOIN chunks_lore ON lore.id = chunks_lore.lore_id
            INNER JOIN chunks ON chunks_lore.chunk_id = chunks.id
            WHERE chunks.community_id = :community_id{additional_conditions}
            """

        # Optionally you'd want to see the other involved chunks
        if return_involved_chunks:
            other_fields += ", chunks.name"

        # Add involved chunks to the query
        for i, chunk_name in enumerate(involved_chunk_names):
            if i > 0:
                other_conditions += " OR "

            var_name: str = f"involved_chunk_name{i}"

            query_vars[var_name] = chunk_name
            other_conditions += f"chunks.name = :{var_name}"

        # Do the query
        results: List[Tuple] = conn.execute(
            sqlalchemy.text(make_query()), [query_vars]
        ).fetchall()

    # Collapse everything into List[LoreView]
    lore_views: List[Lore] = []

    if return_involved_chunks:
        df = pd.DataFrame(results, columns=["lore_text", "involved_chunk_name"])
        groupby_lore = df.groupby("lore_text")

        for result in results:
            lore: str = result[0]

            lore_view: Lore = Lore(
                lore_text=lore,
                about_chunks=groupby_lore.get_group(lore)[
                    "involved_chunk_name"
                ].tolist(),
            )
            lore_views.append(lore_view)
    else:
        lore_views = [Lore(lore_text=result[0], about_chunks=[]) for result in results]

    return lore_views


def view_lore(
    community_id: int,
    involved_chunk_names: List[str] = [],
    involved_chunks_logic: LogicMode = LogicMode.OR,
    return_involved_chunks: bool = False,
) -> List[Lore]:
    def retrieve_lore_individually(set_op: Callable[[Set, Set], Set]) -> List[Lore]:
        # TODO: make this better cuz this is inefficient
        lore_set: Set[Lore] = set(
            retrieve_lore(
                community_id,
                involved_chunk_names=involved_chunk_names[0:1],
                return_involved_chunks=return_involved_chunks,
            )
        )

        for involved_chunk_name in involved_chunk_names[1:]:
            new_lore_set: Set[Lore] = set(
                retrieve_lore(
                    community_id,
                    involved_chunk_names=[involved_chunk_name],
                    return_involved_chunks=return_involved_chunks,
                )
            )

            lore_set = set_op(lore_set, new_lore_set)

        return list(lore_set)

    # NOTE: Function logic actually starts here
    if involved_chunks_logic == LogicMode.OR:
        return retrieve_lore(
            community_id,
            involved_chunk_names=involved_chunk_names,
            return_involved_chunks=return_involved_chunks,
        )
    elif involved_chunks_logic == LogicMode.AND:
        return retrieve_lore_individually(lambda a, b: a & b)
    elif involved_chunks_logic == LogicMode.XOR:
        return retrieve_lore_individually(lambda a, b: a ^ b)

    # Otherwise, raise an error
    raise Exception(
        "Bruh moment: use one of the valid LogicMode values for involved_chunks_logic"
    )


# CLEANUP
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
            conn.execute(sqlalchemy.text(query), [dict(community_id=community_id)])

    return "OK"


# UTIL
# --------


def get_user_id(user_email: str) -> int | None:
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT id FROM users WHERE email = :email"),
            {"email": user_email},
        ).first()

    if result is None:
        return None
    else:
        return result[0]


def get_user_email(user_id: int) -> str | None:
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT email FROM users WHERE id = :id"),
            {"id": user_id},
        ).first()

    if result is None:
        return None
    else:
        return result[0]
