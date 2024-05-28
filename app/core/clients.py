import os
from typing import List, Dict, Optional, Union
from fastapi import Depends, HTTPException, status, Request

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


def read_user_client(user_id) -> KindeApiClient:
    global user_clients

    retrieved_serialized_user_api_client = user_clients.get(user_id)
    retrieved_json_user_api_client: Dict = json.loads(
        retrieved_serialized_user_api_client
    )

    user_api_client = KindeApiClient(**retrieved_json_user_api_client)

    return user_api_client


def write_user_client(user_id, client_value: KindeApiClient):
    global user_clients

    serialized_user_api_client = json.dumps(client_value.__dict__)

    user_clients.set(user_id, serialized_user_api_client)


def delete_user_client(user_id):
    global user_clients

    user_clients.delete(user_id)


# Dependency to get the current user's KindeApiClient instance
# Like an ID to a party or something except this party requires being an authenticated user
# We will use dependency injection to GATEKEEP our routes! LOL!!!
def get_kinde_client(request: Request) -> KindeApiClient:
    global user_clients

    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Manifest a session
    if user_clients.get(user_id) is None:
        # If the client does not exist, create a new instance / session
        user_api_client = KindeApiClient()
        write_user_client(user_id, user_api_client)

    kinde_client = user_clients.get(user_id)

    # Ensure the client is authenticated
    if not kinde_client.is_authenticated():
        # delete_user_client(user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You should authenticate yourself NOW!",
        )

    return kinde_client
