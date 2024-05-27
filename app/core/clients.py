from typing import List, Dict, Optional, Union
from fastapi import Depends, HTTPException, status, Request

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType


# TODO: change this to using some managed redis like upstash
user_clients: Dict = {}


# Dependency to get the current user's KindeApiClient instance
# We will use dependency injection to GATEKEEP our routes! LOL!!!
def get_kinde_client(request: Request) -> KindeApiClient:
    global user_clients

    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Manifest it
    if user_id not in user_clients:
        # If the client does not exist, create a new instance
        user_clients[user_id] = KindeApiClient()

    kinde_client = user_clients[user_id]

    # Ensure the client is authenticated
    if not kinde_client.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    return kinde_client
