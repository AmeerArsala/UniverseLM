import os
from typing import List, Dict, Optional, Union, Any
from authlib.oauth2.auth import OAuth2Token
from fastapi import Depends, HTTPException, status, Request

from pydantic import BaseModel

from app import config

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType

import redis
import json


# Kinde client configuration (for server)
configuration: Configuration = Configuration(host=config.KINDE_ISSUER_URL)
kinde_api_client_params: Dict = config.init_kinde_api_client_params(configuration)

# USER KINDE CLIENTS FOR USER SESSIONS
user_clients = redis.Redis(
    host=os.getenv("UPSTASH_REDIS_HOST_USERSESSIONS"),
    port=6379,
    password=os.getenv("UPSTASH_REDIS_PASSWORD_USERSESSIONS"),
    ssl=True,
)


class KindeApiClientData(BaseModel):
    access_token_obj: Any
    token_endpoint: str
    # audience: Optional[Any]

    def as_api_client(self) -> KindeApiClient:
        api_client: KindeApiClient = KindeApiClient(**kinde_api_client_params)
        OAuth2Token
        # For access token
        api_client._KindeApiClient__access_token_obj = OAuth2Token.from_dict(
            self.access_token_obj
        )
        api_client.configuration.access_token = self.access_token_obj.get(
            "access_token"
        )
        api_client.token_endpoint = self.token_endpoint

        return api_client


def read_user_client(user_auth_id: str) -> KindeApiClient:
    global user_clients

    retrieved_serialized_data = user_clients.get(user_auth_id)
    retrieved_deserialized_client_data: Dict = json.loads(retrieved_serialized_data)

    user_api_client_data: KindeApiClientData = KindeApiClientData(
        **retrieved_deserialized_client_data
    )

    # Now reproduce the client
    user_api_client: KindeApiClient = user_api_client_data.as_api_client()

    return user_api_client


def write_user_client(user_auth_id: str, client: KindeApiClient):
    global user_clients

    # print(f"Writing user client {user_id}...")

    user_api_client_data: KindeApiClientData = KindeApiClientData(
        access_token_obj=client._KindeApiClient__access_token_obj,
        token_endpoint=client.token_endpoint,
        audience=client.audience,
    )

    # print(f"Dict to upload: {user_api_client_data.dict()}")
    user_api_client_data_dict: Dict = user_api_client_data.dict()

    serialized_user_api_client_data = json.dumps(user_api_client_data_dict)
    user_clients.set(
        user_auth_id,
        serialized_user_api_client_data,
        # Expires in X seconds
        ex=user_api_client_data_dict["access_token_obj"]["expires_in"],
    )


def delete_user_client(user_auth_id: str):
    global user_clients

    user_clients.delete(user_auth_id)


# Will expire as soon as it is read
# Otherwise, has a short expiration time
def readex_user_auth_id(state: str) -> str:
    global user_clients

    # Have it expire as soon as it is read
    user_auth_id: str = user_clients.getex(state, px=10)  # expire after 10 ms
    # retrieved_serialized_data = user_clients.getex(state, ex=0)
    # retrieved_deserialized_client_data: Dict = json.loads(retrieved_serialized_data)

    return user_auth_id


def write_user_auth_id(state: str, user_auth_id: str):
    global user_clients

    # Short expiration; 15 secs
    user_clients.set(state, user_auth_id, ex=15)


def get_user_session_client(request: Request, manifest: bool = False) -> KindeApiClient:
    global user_clients

    user_id = request.session.get("user_id")
    if user_id is None:
        print("User ID not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    user_api_client: KindeApiClient = None
    should_write_client: bool = False

    # Manifest a session
    if user_clients.get(user_id) is None:
        # If the client does not exist, create a new instance / session
        user_api_client = KindeApiClient()
        should_write_client = True
        # write_user_client(user_id, user_api_client)
    else:
        user_api_client = read_user_client(user_id)

    # Ensure the client is authenticated
    if not user_api_client.is_authenticated():
        # delete_user_client(user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You should authenticate yourself NOW!",
        )

    if manifest and should_write_client:
        write_user_client(user_id, user_api_client)

    return user_api_client


# Dependency to get the current user's KindeApiClient instance
# Like an ID to a party or something except this party requires being an authenticated user
# We will use dependency injection to GATEKEEP our routes! LOL!!!
def get_user_kinde_client(request: Request) -> KindeApiClient:
    return get_user_session_client(request, manifest=True)
