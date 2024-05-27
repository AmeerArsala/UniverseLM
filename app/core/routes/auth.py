from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app import config
from app.core import clients

from kinde_sdk.kinde_api_client import KindeApiClient


router = APIRouter()


# Login endpoint
@router.get("/login")
def login(request: Request):
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    login_url = kinde_client.get_login_url()

    return RedirectResponse(login_url)


# Register endpoint
@router.get("/register")
def register(request: Request):
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    register_url = kinde_client.get_register_url()

    return RedirectResponse(register_url)


# Post-login/register: where to go? (I think)
@router.get("/kinde_callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))

    user = kinde_client.get_user_details()
    user_id = user.get("id")

    # Store in session
    request.session["user_id"] = user_id

    # Update the user_clients cache with the client
    clients.write_user_client(user_id, kinde_client)

    return RedirectResponse(router.url_path_for("read_root"))


# Logout endpoint
@router.get("/logout")
def logout(request: Request):
    # First, let's get the user_id
    user_id = request.session.get("user_id")

    # Now, let's log this mf out
    if user_id in clients.user_clients:
        kinde_user_client = clients.read_user_client(user_id)

        # LOG EM OUT
        logout_url = kinde_user_client.logout(redirect_to=config.LOGOUT_REDIRECT_URL)

        # REMOVE ALL TRACES OF EM!!!
        clients.delete_user_client(user_id)
        request.session.pop("user_id", None)

        # LOG EM OUT
        return RedirectResponse(logout_url)

    # Otherwise, unauthorized logout
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="AUTHENTICATE YOURSELF YOU SCOUNDREL!",
    )
