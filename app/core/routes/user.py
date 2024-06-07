from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core import clients, api_auth
from app.core.schemas.users import UserDetails

from app.lib import society, users, states

# import sqlalchemy
# import app.core.db.database as db

from kinde_sdk.kinde_api_client import KindeApiClient


# prefix: /user
router = APIRouter(
    tags=["user stuff (not relating to the simulation itself)"],
    dependencies=[Depends(clients.get_user_kinde_client)],
)


def user_kinde_client(request_url) -> KindeApiClient:
    user_client: KindeApiClient = KindeApiClient(**clients.kinde_api_client_params)
    user_client.fetch_token(authorization_response=str(request_url))

    return user_client


@router.post("/create_apikey")
async def create_api_key(request: Request) -> str:
    user_client = user_kinde_client(request.url)
    user_details: UserDetails = UserDetails(**user_client.get_user_details())

    # user_auth_id: str = user_details.id

    # Make api key and store it
    api_key: str = api_auth.create_api_key(user_details.email)

    return api_key


@router.get("/view_details")
async def view_user_details(request: Request) -> UserDetails:
    user_client: KindeApiClient = user_kinde_client(request.url)

    user_details_dict: Dict[str, str] = user_client.get_user_details()
    return UserDetails(**user_details_dict)


@router.get("/view_details/email")
async def view_user_email(request: Request) -> str:
    user_client: KindeApiClient = user_kinde_client(request.url)

    user_details_dict: Dict[str, str] = user_client.get_user_details()
    return UserDetails(**user_details_dict).email


@router.get("/view_details/user_core_id")
async def view_user_id(request: Request) -> int:
    user_client: KindeApiClient = user_kinde_client(request.url)

    user_details_dict: Dict[str, str] = user_client.get_user_details()
    user_details: UserDetails = UserDetails(**user_details_dict)

    user_id: int = society.get_user_id(user_details.email)

    return user_id


@router.post("/manifest")
async def manifest_user(request: Request) -> int:
    """Returns the user_id"""
    # Get the corresponding email to get the corresponding user_id
    # user_client: KindeApiClient = clients.read_user_client(params.user_auth_id)
    user_client: KindeApiClient = user_kinde_client(request.url)

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
