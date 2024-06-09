from typing import List, Dict, Optional
from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader

import os
import dotenv

import requests

from app.lib.utils import cryptography

import pandas as pd


dotenv.load_dotenv()

# Admin API Keys
admin_api_keys: List[str] = []

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

    keys: List[str] = [result["name"] for result in results]

    # Filter out the emails from the keys
    keys_series = pd.Series(keys)

    # Filter the series to exclude strings containing '@'
    api_keys: List[str] = keys_series[~keys_series.str.contains("@")].tolist()

    return api_keys


# The KV is str -> str
def _read_key(key_name: str) -> str | None:
    account_id: str = CLOUDFLARE_ACCOUNT_ID
    namespace_id: str = CLOUDFLARE_KV_NAMESPACE_ID

    headers = {"Authorization": "Bearer undefined", "Content-Type": "application/json"}

    # Get response from api
    response = requests.get(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}",
        headers=headers,
    )

    value: str = response.json()
    print(value)

    return value


def read_api_key_from_email(email: str) -> str | None:
    api_key: str | None = _read_key(email)

    return api_key


def read_email_from_api_key(api_key: str) -> str:
    user_email: str = _read_key(api_key)

    return user_email


def create_api_key(user_email: str, expiration_ttl: int = -1) -> str:
    # Generate it first
    api_key: str = cryptography.generate_api_key()

    # Put it in the KV DB
    account_id: str = CLOUDFLARE_ACCOUNT_ID
    namespace_id: str = CLOUDFLARE_KV_NAMESPACE_ID

    def make_url(key_name: str) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}"

    headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": "Bearer undefined",
    }

    def make_request(key: str, val, expiration_ttl: int = -1):
        url: str = make_url(key_name=key)

        body = {"metadata": {}, "value": val}

        if expiration_ttl != -1:
            body["expiration_ttl"] = expiration_ttl

        response = requests.request("PUT", url, headers=headers, json=body)
        return response

    # Forward mapping: [user_email -> api_key]
    (K, V) = (user_email, api_key)
    response = make_request(K, V, expiration_ttl=expiration_ttl)

    # Print results of call
    print("Forward Mapping:")
    print(response.status_code)
    print(response.text)

    # Reverse Mapping: [api_key -> user_email]
    (K, V) = (api_key, user_email)
    response = make_request(K, V, expiration_ttl=expiration_ttl)

    # Print results of call
    print("Reverse Mapping:")
    print(response.status_code)
    print(response.text)

    # return it
    return api_key


# User API Keys
user_api_key_header = APIKeyHeader(name="User-API-Key", auto_error=False)


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
api_key_header = APIKeyHeader(name="UniverseLM-API-Key", auto_error=False)


async def get_api_key(request: Request, api_key_header: str = Security(api_key_header)):
    global admin_api_keys

    user_api_keys: List[str] = get_all_user_api_keys()
    all_api_keys: List[str] = admin_api_keys + user_api_keys

    if api_key_header in all_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )
