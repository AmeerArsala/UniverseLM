from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from app.core import clients, api_auth

from kinde_sdk.kinde_api_client import KindeApiClient


router = APIRouter(
    tags=["user stuff (not relating to the simulation itself)"],
    dependencies=[Depends(clients.get_kinde_client)],
)


@router.post("/create_apikey")
async def create_api_key(request: Request) -> str:
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))

    user = kinde_client.get_user_details()
    user_id = user.get("id")

    # Make api key and store it
    api_key: str = api_auth.create_api_key(user_id)

    return api_key
