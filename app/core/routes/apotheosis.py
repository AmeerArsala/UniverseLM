from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core import api_auth

from app.core.schemas.entities import Chunk

from app.lib import society, states

import sqlalchemy
import app.core.db.database as db


# prefix: /apotheosis
router = APIRouter(tags=["apotheosis"], dependencies=[Depends(api_auth.get_api_key)])


class CreateCommunityParams(BaseModel):
    name: str


@router.post("/community")
async def create_community(params: CreateCommunityParams) -> int:
    community_id: int = society.create_community(params.name)

    return community_id


class CreateChunksParams(BaseModel):
    chunks: List[Chunk]


@router.post("/chunks")
async def create_chunks(params: CreateChunksParams):
    society.create_chunks(params.chunks)

    return "OK"


class JoinCommunityParams(BaseModel):
    community_name: str
    user_email: str


# NOTE: 2 things need to be enforced here
# 1 - the user_email must be the same one they are using. This can be done by tying the API key to their email address in a KV storage
# 2 - if the community is not public (if it doesn't have a '/' in the id), they will need to have the correct perms to access it
@router.post("/community/join")
async def join_community(
    params: JoinCommunityParams, api_key: str = Depends(api_auth.get_api_key)
):
    # It is already assumed that a valid api key exists by virtue of this route
    email: str = api_auth.read_email_from_api_key(api_key)

    # 1
    if email != params.user_email:
        return "Bruh use your own email stop tryna use other ppls accounts"

    # Action
    def join():
        society.join_community(
            user_email=params.user_email, community_name=params.community_name
        )

    # 2
    is_public: bool = "/" not in params.community_name
    if is_public:
        join()
        return "OK"

    can_access_community: bool = False

    with db.engine.begin() as conn:
        # Get community id first
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            {"name": params.community_name},
        ).first()

        query: str = """
        SELECT COUNT(eligible_users_for_communities.user_id)
        FROM users INNER JOIN eligible_users_for_communities ON users.id = eligible_users_for_communities.user_id
        WHERE users.email = :email AND eligible_users_for_communities.community_id = :community_id
        """

        (num,) = conn.execute(
            sqlalchemy.text(query), {"email": email, "community_id": community_id}
        ).first()
        can_access_community = num > 0

    if can_access_community:
        join()
        return "OK"
    else:
        return "Access Denied"


class WhitelistUsersParams(BaseModel):
    whitelisted_emails: List[str]
    community_name: str


# ONLY allow this to be called on private communities.
# Therefore, the assumption is that the community is private
# Also check if the requestor has owner perms
# (Like on the front end don't even let the option appear if the community is public)
@router.post("/community/whitelist")
async def whitelist_users(
    params: WhitelistUsersParams, api_key: str = Depends(api_auth.get_api_key)
):

    with db.engine.begin() as conn:
        # Get community id first
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            {"name": params.community_name},
        ).first()

        query: str = """
        INSERT INTO eligible_users_for_communities(user_id, community_id)
        SELECT DISTINCT users.id, :community_id
        FROM users
        WHERE users.email IN :emails
        """

        # Execute the insertion
        conn.execute(
            sqlalchemy.text(query),
            {"community_id": community_id, "emails": tuple(params.whitelisted_emails)},
        )

    return "OK"


class PromoteOwnersParams(BaseModel):
    new_owners_emails: List[str]
    community_name: str


@router.post("/community/add_owners")
async def promote_owners(
    params: PromoteOwnersParams, api_key: str = Depends(api_auth.get_api_key)
):
    # NOTE: same thing as the function above, just with adding to `communities_owners` rather than `eligible_users_for_communities`
    with db.engine.begin() as conn:
        # Get community id first
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            {"name": params.community_name},
        ).first()

        query: str = """
        INSERT INTO communities_owners(user_id, community_id)
        SELECT DISTINCT users.id, :community_id
        FROM users
        WHERE users.email IN :emails
        """

        # Execute the insertion
        conn.execute(
            sqlalchemy.text(query),
            {"community_id": community_id, "emails": tuple(params.new_owners_emails)},
        )

    return "OK"
