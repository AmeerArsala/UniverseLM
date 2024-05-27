from typing import List, Dict, Optional
from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader

import os
import dotenv

import requests

from app.lib.utils import cryptography


dotenv.load_dotenv()

# Admin API Keys
admin_api_keys: List = []

admin_api_keys.append(os.environ.get("ADMIN_API_KEY"))
admin_api_key_header = APIKeyHeader(name="admin_access_token", auto_error=False)


async def get_admin_api_key(
    request: Request, api_key_header: str = Security(admin_api_key_header)
):
    if api_key_header in admin_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_KV_NAMESPACE_ID = os.getenv("CLOUDFLARE_KV_NAMESPACE_ID")


def get_all_user_api_keys() -> List[str]:
    account_id: str = CLOUDFLARE_ACCOUNT_ID
    namespace_id: str = CLOUDFLARE_KV_NAMESPACE_ID

    headers = {"Authorization": "Bearer undefined", "Content-Type": "application/json"}

    # Get response from api
    response: Dict = requests.get(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/keys",
        headers=headers,
    )

    results: List[Dict] = response["result"]

    api_keys: List[str] = [result["name"] for result in results]

    return api_keys


# user_id is hopefully a string
def create_api_key(user_id) -> str:
    # Generate it first
    api_key: str = cryptography.generate_api_key()

    # Put it in the KV DB
    account_id: str = CLOUDFLARE_ACCOUNT_ID
    namespace_id: str = CLOUDFLARE_KV_NAMESPACE_ID

    headers = {"Authorization": "Bearer undefined", "Content-Type": "application/json"}

    query_params = {"base64": False, "key": user_id, "value": api_key}

    response = requests.put(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk",
        headers=headers,
        params=query_params,
    )

    # Print results of call
    print(response.status_code)
    print(response.text)

    # return it
    return api_key


# User API Keys
user_api_key_header = APIKeyHeader(name="user_access_token", auto_error=False)


async def get_user_api_key(
    request: Request, api_key_header: str = Security(user_api_key_header)
):
    user_api_keys: List[str] = get_all_user_api_keys()

    if api_key_header in user_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


# Now, for ALL api keys (admin api key is a God token)
api_key_header = APIKeyHeader(name="universal_access_token", auto_error=False)


async def get_api_key(request: Request, api_key_header: Security(api_key_header)):
    global admin_api_keys

    user_api_keys: List[str] = get_all_user_api_keys()
    all_api_keys: List[str] = admin_api_keys + user_api_keys

    if api_key_header in all_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )
