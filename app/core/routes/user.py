from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core import clients, api_auth
from app.core.schemas.users import TierPlan, UserDetails

from app.lib import society, users, states

# import sqlalchemy
# import app.core.db.database as db

from kinde_sdk.kinde_api_client import KindeApiClient


# prefix: /user
# full prefix: /user/{user_auth_id}
router = APIRouter(
    prefix="/{user_auth_id}",
    tags=["user stuff (not relating to the simulation itself)"],
    dependencies=[Depends(clients.get_user_kinde_client)],
)


def _get_user_details(user_auth_id: str) -> UserDetails:
    user_client: KindeApiClient = clients.read_user_client(user_auth_id)

    print("GETTING USER DETAILS...")
    user_details_dict: Dict[str, str] = user_client.get_user_details()
    print(user_details_dict)

    return UserDetails(**user_details_dict)


@router.post("/create_apikey")
async def create_api_key(user_auth_id: str, expiration_ttl_seconds: int) -> str:
    user_client = clients.read_user_client(user_auth_id)
    user_details: UserDetails = UserDetails(**user_client.get_user_details())

    # user_auth_id: str = user_details.id
    expiration_ttl: int = expiration_ttl_seconds

    # 'int'ify it
    if expiration_ttl is None:
        expiration_ttl = -1
    else:
        expiration_ttl = int(expiration_ttl)

    # Make api key and store it
    api_key: str = api_auth.create_api_key(
        user_details.email, expiration_ttl=expiration_ttl
    )

    return api_key


# using post for the additional security
@router.post("/get_apikey")
async def get_api_key(user_auth_id: str) -> str:
    user_client = clients.read_user_client(user_auth_id)
    user_details: UserDetails = UserDetails(**user_client.get_user_details())

    print("READING API KEY...")
    api_key: str | None = api_auth.read_api_key_from_email(user_details.email)

    print(f"API KEY: {api_key}")

    if api_key is None:
        print("NO API KEY FOUND")
        return "null"

    return api_key


@router.get("/view_details")
async def view_user_details(user_auth_id: str) -> UserDetails:
    user_details: UserDetails = _get_user_details(user_auth_id)

    return user_details


@router.get("/view_details/email")
async def view_user_email(user_auth_id: str) -> str:
    user_details: UserDetails = _get_user_details(user_auth_id)
    return user_details.email


@router.get("/view_details/user_core_id")
async def view_user_id(user_auth_id: str) -> int:
    user_details: UserDetails = _get_user_details(user_auth_id)
    user_id: int = society.get_user_id(user_details.email)

    return user_id


@router.get("/view_profile/readme")
async def get_user_readme(user_auth_id: str) -> str:
    user_details: UserDetails = _get_user_details(user_auth_id)

    print("Getting user profile README...")
    README: str = society.get_user_readme(user_details.email)

    return README


@router.get("/view_profile/tier_plan")
async def get_user_tier_plan(user_auth_id: str) -> int:
    user_details: UserDetails = _get_user_details(user_auth_id)

    plan = society.get_user_tier_plan_from_email(user_details.email)
    if plan is None:
        plan = TierPlan.FREE_TIER

    tier_plan: int = int(plan)

    return tier_plan


@router.post("/manifest")
async def manifest_user(user_auth_id: str) -> int:
    """Returns the user_id"""
    # Get the corresponding email to get the corresponding user_id
    # user_client: KindeApiClient = clients.read_user_client(params.user_auth_id)
    user_client: KindeApiClient = clients.read_user_client(user_auth_id)

    user_details: UserDetails = UserDetails(**user_client.get_user_details())
    email: str = user_details.email

    # Check the DB to see if the user already exists. If so, then grab and return the user_id
    print("Checking to see if user already exists...")
    user_id_result = society.get_user_id(email)

    user_id: int = -1
    if user_id_result is not None:
        print("User already exists")
        user_id = user_id_result
    else:
        # Otherwise, make a new user
        print("User does not exist. Creating new user...")
        user_id = society.create_user(email)

    return user_id
