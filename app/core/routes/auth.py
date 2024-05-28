from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from app import config
from app.core import clients


from kinde_sdk.kinde_api_client import KindeApiClient


router = APIRouter(tags=["auth"])


# Login endpoint
# Call this to get the link to login
@router.get("/login")
def login(request: Request):
    # Decipher query params first
    method: str = request.query_params["method"]

    print(method)

    auth_params: Dict = {"connection_id": config.CONNECTION_IDS[method]}

    if method == "email_password":
        email: str = request.query_params["email"]
        auth_params["login_hint"] = email

    # print(auth_params)

    # Construct the redirect with the extra params
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    login_url = kinde_client.get_login_url(
        additional_params={"auth_url_params": auth_params}
    )

    # print(login_url)

    return RedirectResponse(login_url)


# Register endpoint
# Call this to get the link to register
@router.get("/register")
def register(request: Request):
    # Decipher query params first
    method: str = request.query_params["method"]

    # print(method)

    auth_params: Dict = {"connection_id": config.CONNECTION_IDS[method]}

    if method == "email_password":
        email: str = request.query_params["email"]
        auth_params["login_hint"] = email

    # print(auth_params)

    # Construct the redirect with the extra params
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    register_url = kinde_client.get_register_url(
        additional_params={"auth_url_params": auth_params}
    )

    return RedirectResponse(register_url)


# I believe this is post-login/register, but not logout
# In which case, it should attempt to write a user client session
# As a result, the front end should probably invoke serverless functions to handle what is covered/implied by the /login and /register routes above and then call this route
# Call this on when the redirect happens at https://universelm.org/callback
@router.get("/kinde_callback")
def callback(request: Request):
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))

    user = kinde_client.get_user_details()
    user_id = user.get("id")

    # Store in session
    request.session["user_id"] = user_id

    # Update the user_clients cache with the client session
    clients.write_user_client(user_id, kinde_client)

    # return RedirectResponse(config.KINDE_CALLBACK_URL)
    # This is for after the the /callback is navigated to on the front end, which will then call this function
    # From there, it will navigate back to the original
    # return RedirectResponse(app_global.url_path_for("read_root"))
    return RedirectResponse(config.SITE_URL)


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

        # REMOVE ALL TRACES OF 'EM!!!
        clients.delete_user_client(user_id)
        request.session.pop("user_id", None)

        # LOG EM OUT
        return RedirectResponse(logout_url)

    # Otherwise, unauthorized logout
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="AUTHENTICATE YOURSELF YOU SCOUNDREL!",
    )
