from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core import clients, api_auth
from app.core.schemas.users import UserDetails

from app.lib import society, users, states

import sqlalchemy
import app.core.db.database as db

from kinde_sdk.kinde_api_client import KindeApiClient


router = APIRouter(
    tags=["user stuff (not relating to the simulation itself)"],
    dependencies=[Depends(clients.get_user_kinde_client)],
)


@router.post("/create_apikey")
async def create_api_key(request: Request) -> str:
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))

    user = kinde_client.get_user_details()
    user_auth_id = user.get("id")

    # Make api key and store it
    api_key: str = api_auth.create_api_key(user_auth_id)

    return api_key


@router.get("/view_details")
async def view_user_details(user_auth_id: str) -> UserDetails:
    kinde_client: KindeApiClient = clients.read_user_client(user_auth_id)

    user_details_dict: Dict[str, str] = kinde_client.get_user_details()
    return UserDetails(**user_details_dict)


class ManifestUserParams(BaseModel):
    user_auth_id: str


@router.post("/manifest")
async def manifest_user(params: ManifestUserParams) -> int:
    """Returns the user_id"""
    # Get the corresponding email to get the corresponding user_id
    user_client: KindeApiClient = clients.read_user_client(params.user_auth_id)

    user_details: UserDetails = UserDetails(**user_client.get_user_details())
    email: str = user_details.email

    # Check the DB to see if the user already exists. If so, then grab and return the user_id
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("SELECT id FROM users WHERE email = :email"),
            {"email": email},
        ).first()

    user_id: int = -1
    if result is not None:
        user_id = result[0]
    else:
        # Otherwise, make a new user
        user_id = society.create_user(email)

    return user_id
