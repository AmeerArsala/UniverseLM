from typing import List, Dict, Optional
from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader

import os
import dotenv


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


# User API Keys
# TODO: change to using redis and getting the list of all OK'd api keys
user_api_keys: List = []
user_api_key_header = APIKeyHeader(name="user_access_token", auto_error=False)


async def get_user_api_key(
    request: Request, api_key_header: str = Security(user_api_key_header)
):
    # TODO: pull down the list of all OK'd api keys from upstash
    if api_key_header in user_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


# Now, for ALL api keys (admin api key is a God token)
all_api_keys: List = admin_api_keys + user_api_keys
api_key_header = APIKeyHeader(name="universal_access_token", auto_error=False)


async def get_api_key(request: Request, api_key_header: Security(api_key_header)):
    if api_key_header in all_api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )
