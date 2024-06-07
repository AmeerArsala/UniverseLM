from typing import Union, Optional, List, Dict, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core import api_auth

from app.core.schemas.entities import Chunk
from app.core.schemas.users import TierPlan

from app.lib import society, states

import sqlalchemy
import app.core.db.database as db

import re

import numpy as np
import pandas as pd


# prefix: /apotheosis
router = APIRouter(tags=["apotheosis"], dependencies=[Depends(api_auth.get_api_key)])


class CreateCommunityParams(BaseModel):
    name: str
    private: bool

    ai_generate_base: bool = Field(default=False)
    # these fields don't matter unless ai_generate_base is True
    # these are the default values of the corresponding arguments in society.generate_chunks, so don't touch them
    community_desc: str = Field(default="")
    num_chunks: int = Field(default=-1)

    invited_owners_emails: List[str] = Field(default=[])

    # this doesn't matter unless private is True
    invited_whitelisted_emails: List[str] = Field(default=[])


class CreateCommunityResponse(BaseModel):
    success: bool
    name_allowed: bool = Field(default=True)
    privacy_allowed: bool = Field(default=True)

    # these return "OK" if they are allowed and an error message otherwise
    name_status_message: str = Field(default="OK")
    privacy_status_message: str = Field(default="OK")

    community_id: int = Field(default=-1)


@router.post("/community")
async def create_community(
    params: CreateCommunityParams, api_key: str = Depends(api_auth.get_api_key)
) -> CreateCommunityResponse:
    # This is done so the user doesn't go around fucking with other users' accounts
    print("Reading API Key...")
    email: str = api_auth.read_email_from_api_key(api_key)

    response_dict: Dict = {}
    success: bool = True

    print("Validating Community parameters...")
    # Check if the privacy option they chose is allowed
    if (
        params.private
        and society.get_user_tier_plan_from_email(email) < TierPlan.PRO_TIER
    ):
        response_dict["privacy_allowed"] = False
        response_dict["privacy_status_message"] = (
            "You must be on a paid plan (Pro or beyond) to create private societies"
        )
        success = False
    # else:
    #     response_dict["privacy_allowed"] = True
    #     response_dict["privacy_status_message"] = "OK"

    # Now, check if the name is valid
    def is_valid_name(name: str) -> bool:
        # Define a regular expression that matches lowercase letters, numbers, and hyphens
        pattern = re.compile(r"^[a-z0-9-]+$")

        # Check if the name matches the pattern
        return bool(pattern.match(name))

    # Assumes `name` has valid chars
    def complete_name(name: str) -> str:
        return f"{email}/{name}" if params.private else name

    def is_name_available(name: str) -> bool:
        full_name: str = complete_name(name)

        return society.is_community_name_available(full_name)

    if not is_valid_name(params.name):
        response_dict["name_allowed"] = False
        response_dict["name_status_message"] = (
            "Names can only consist of lowercase letters, digits, and hyphens (-)"
        )
        success = False
    elif success and not is_name_available(params.name):
        response_dict["name_allowed"] = False
        response_dict["name_status_message"] = (
            f"{complete_name(params.name)} is unavailable or already taken"
        )
        success = False

    if not success:
        print("Creation of Community failed. Parameters invalid")
        return CreateCommunityResponse(success=False, **response_dict)

    # Otherwise, success is True and create the community!
    print("Parameters valid. Creating Community...")
    community_id: int = society.create_community(params.name)

    # Generate and add chunks if specified
    if params.ai_generate_base:
        print("Generating chunks...")
        generated_chunks: List[Chunk] = society.generate_chunks(
            community_id, desc=params.community_desc, count=params.num_chunks
        )

        print("Uploading generated chunks...")
        society.create_chunks(generated_chunks)

    # Invite people

    # Normalize
    print("Adding owner(s)...")
    added_owners_emails: List[str] = params.invited_owners_emails + email
    added_owners_emails = pd.unique(np.array(added_owners_emails)).tolist()

    society.add_community_owners(community_id, added_owners_emails)

    if params.private:
        print("Adding user(s) to whitelist...")

        # Normalize
        added_whitelist_emails: List[str] = pd.unique(
            # add owners emails because all owners must be whitelisted too in order to even enter the society
            np.array(params.invited_whitelisted_emails + added_owners_emails)
        ).tolist()

        society.add_users_to_community_whitelist(
            community_id, added_whitelist_emails, bypass_privacy_check=True
        )

    # Have OG user join the community
    print("Joining Community...")
    society.join_community_by_id(email, community_id)

    return CreateCommunityResponse(
        success=True, community_id=community_id, **response_dict
    )


class CreateChunksParams(BaseModel):
    chunks: List[Chunk]


@router.post("/chunks")
async def create_chunks(
    params: CreateChunksParams, api_key: str = Depends(api_auth.get_api_key)
):
    """Constraint: users can only create chunks in communities they have joined."""
    print("Reading API Key...")
    email: str = api_auth.read_email_from_api_key(api_key)

    # Find out whether user is in the communities to be able to create chunks in them
    print("Filtering chunks to add to only the ones the user is allowed to add...")
    desired_community_ids: List[int] = [chunk.community_id for chunk in params.chunks]
    with db.engine.begin() as conn:
        query = """
        SELECT users_communities.community_id
        FROM users INNER JOIN users_communities ON users.id = users_communities.user_id
        WHERE users.email = :email AND users_communities.community_id IN :desired_community_ids
        """

        results: List[Tuple[int]] = conn.execute(
            sqlalchemy.text(query),
            [{"email": email, "desired_community_ids": tuple(desired_community_ids)}],
        ).fetchall()

    available_community_ids: List[int] = [result[0] for result in results]

    # THESE are the chunks to create
    filtered_chunks: List[Chunk] = list(
        filter(
            lambda chunk: (chunk.community_id in set(available_community_ids)),
            params.chunks,
        )
    )

    if len(filtered_chunks) > 0:
        print("Only adding the chunks that the user is allowed to add...")
        society.create_chunks(filtered_chunks)

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
    print("Reading API Key...")
    email: str = api_auth.read_email_from_api_key(api_key)

    # 1
    if email != params.user_email:
        return "BRUH MOMENT EXCEPTION: use your own damn email stop tryna use other ppls accounts"

    # 2 - join if can access
    print("Seeing if user can access community...")
    can_access_community: bool = society.user_can_access_community(
        params.community_name, params.user_email
    )

    if can_access_community:
        print("Joining community...")
        society.join_community(params.user_email, params.community_name)
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
    # Check if requesting user has owner perms
    user_email: str = api_auth.read_email_from_api_key(api_key)

    with db.engine.begin() as conn:
        # Get community id first
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            {"name": params.community_name},
        ).first()

        # Check if user is an owner
        query = """
        SELECT COUNT(*)
        FROM users INNER JOIN communities_owners ON users.id = communities_owners.user_id
        WHERE users.email = :email AND community_owners.community_id = :community_id
        """
        (occurrences_as_owner,) = conn.execute(
            sqlalchemy.text(query),
            [{"email": user_email, "community_id": community_id}],
        ).first()

        if occurrences_as_owner == 0:
            return "Access Denied: You must be an owner to add users to the whitelist"

    society.add_users_to_community_whitelist(community_id, params.whitelisted_emails)

    return "OK"


class PromoteOwnersParams(BaseModel):
    new_owners_emails: List[str]
    community_name: str


@router.post("/community/add_owners")
async def promote_owners(
    params: PromoteOwnersParams, api_key: str = Depends(api_auth.get_api_key)
):
    # NOTE: same thing as the function above, just with adding to `communities_owners` rather than `eligible_users_for_communities`

    # Check if requesting user has owner perms
    user_email: str = api_auth.read_email_from_api_key(api_key)

    with db.engine.begin() as conn:
        # Get community id first
        (community_id,) = conn.execute(
            sqlalchemy.text("SELECT id FROM communities WHERE name = :name"),
            {"name": params.community_name},
        ).first()

        # Check if user is an owner
        query = """
        SELECT COUNT(*)
        FROM users INNER JOIN communities_owners ON users.id = communities_owners.user_id
        WHERE users.email = :email AND community_owners.community_id = :community_id
        """
        (occurrences_as_owner,) = conn.execute(
            sqlalchemy.text(query),
            [{"email": user_email, "community_id": community_id}],
        ).first()

        if occurrences_as_owner == 0:
            return "Access Denied: You must be an owner to add more owners"

    society.add_community_owners(community_id, params.new_owners_emails)

    return "OK"
