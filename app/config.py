import os
from dotenv import load_dotenv
from typing import Dict

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType
from authlib.common.security import generate_token


load_dotenv()

# Must become true on prod
PROD_MODE: bool = os.getenv("MODE") == "PROD"

# Local development params
SITE_HOST: str = "localhost"
SITE_PORT: int = 8080

# Quickstart copy/paste overwrite section
SITE_URL = (
    "https://universelm.vercel.app" if PROD_MODE else f"http://{SITE_HOST}:{SITE_PORT}"
)


LOGOUT_REDIRECT_URL = f"{SITE_URL}/auth/logout"
KINDE_CALLBACK_URL = f"{SITE_URL}/auth/kinde_callback"
CLIENT_ID = os.getenv("KINDE_CLIENT_ID")
CLIENT_SECRET = os.getenv("KINDE_CLIENT_SECRET")

# Quickstart copy/paste overwrite section

KINDE_ISSUER_URL = os.getenv("KINDE_ISSUER_URL")
GRANT_TYPE = GrantType.AUTHORIZATION_CODE_WITH_PKCE  # GrantType.AUTHORIZATION_CODE
CODE_VERIFIER = os.getenv("KINDE_CODE_VERIFIER")  # A suitably long string > 43 chars
TEMPLATES_AUTO_RELOAD = True

# Session Management
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
SECRET_KEY = os.getenv("KINDE_SECRET_KEY")  # Secret used for session management

# with PKCE flow, this is required
CODE_VERIFIER = generate_token(48)


def init_kinde_api_client_params(configuration: Configuration) -> Dict:
    kinde_api_client_params = {
        "configuration": configuration,
        "domain": KINDE_ISSUER_URL,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE,
        "callback_url": KINDE_CALLBACK_URL,
    }

    if GRANT_TYPE == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
        kinde_api_client_params["code_verifier"] = CODE_VERIFIER

    return kinde_api_client_params
