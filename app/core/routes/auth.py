from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import Response, RedirectResponse, HTMLResponse
from starlette.status import HTTP_307_TEMPORARY_REDIRECT, HTTP_301_MOVED_PERMANENTLY
from pydantic import BaseModel, Field

from app import config
from app.core import clients

from kinde_sdk.kinde_api_client import KindeApiClient


router = APIRouter(tags=["auth"])


# Login endpoint
# Call this to get the link to login
@router.get("/login")
def login(request: Request):
    print("LOGGING IN...")

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
    print("REGISTERING...")

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
async def callback(request: Request):
    kinde_client = KindeApiClient(**clients.kinde_api_client_params)
    kinde_client.fetch_token(authorization_response=str(request.url))

    user = kinde_client.get_user_details()

    print(f"user: {user}")

    user_id: str = user.get("id")

    # Store in session
    request.session["user_id"] = user_id

    # Find out whether it is the first time the user is requesting (via this heuristic)
    is_first_time: bool = clients.user_clients.get(user_id) is None

    # Update the user_clients cache with the client session
    clients.write_user_client(user_id, kinde_client)

    redirect_url: str = ""
    if is_first_time:
        redirect_url = config.FIRST_TIME_POST_CALLBACK_REDIRECT_URL
    else:
        redirect_url = config.POST_CALLBACK_REDIRECT_URL

    # js_code: str = f"""
    # localStorage.setItem('userId', '{user_id}');
    # console.log("DONE");
    # """
    #
    # html_content: str = f"""
    # <!DOCTYPE html>
    # <html>
    #     <head>
    #         <meta http-equiv="refresh" content="0; URL='{redirect_url}'" />
    #         <script>
    #             {js_code}
    #         </script>
    #     </head>
    # </html>
    # """

    # return RedirectResponse(app_global.url_path_for("read_root"))
    # return RedirectResponse(redirect_url)
    # return HTMLResponse(content=html_content, status_code=200)

    # Custom response that redirects with a value
    # response = Response(content=user_id, media="text/plain")
    # response.status_code = HTTP_301_MOVED_PERMANENTLY
    # response.headers["Location"] = redirect_url

    response = RedirectResponse(redirect_url)
    response.set_cookie(key="user_id", value=user_id)

    return response


# Logout endpoint
@router.get("/logout")
async def logout(request: Request):
    print("LOGGING OUT...")

    # First, let's get the user_id
    user_id = request.session.get("user_id")

    # Now, let's log this mf out
    if (user_id is not None) and (clients.user_clients.get(user_id) is not None):
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


@router.get("/is_authenticated")
async def get_is_authenticated(request: Request) -> bool:
    print("CHECKING AUTHENTICATION STATE...")
    # print(request.query_params)

    # First, get the user_id
    user_id: str = request.query_params["user_id"]

    if user_id is None:
        print("User ID not found")
        return False

    # Next, get the corresponding client
    user_client: KindeApiClient = clients.read_user_client(user_id)

    # Finally, check the authentication state
    is_authenticated: bool = user_client.is_authenticated()

    print(is_authenticated)

    return is_authenticated
