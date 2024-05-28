import os
from sys import prefix
from typing import Union, Optional, List, Dict

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Request,
    APIRouter,
    exceptions,
)
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from kinde_sdk.kinde_api_client import KindeApiClient

from fastapi.responses import JSONResponse
from pydantic import ValidationError

import json
import logging

# import uvicorn

from app import config
from app.core import clients
from app.core.routes import apotheosis, chat, functions, dataview, admin, auth, user
from app.lib import society, states, users


description = """
UniverseLM is All You Need
"""

app = FastAPI(
    title="UniverseLM",
    description=description,
    version="0.0.1",
    terms_of_service="https://ran.anemo.ai",
    contact={"name": "Ameer Arsala", "email": "aarsala@calpoly.edu"},
)

# For now, allow all
origin_whitelist = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origin_whitelist,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session/Auth management
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)


app.include_router(apotheosis.router, prefix="/apotheosis")
app.include_router(chat.router, prefix="/chat")
app.include_router(functions.router, prefix="/community")
app.include_router(dataview.router, prefix="/view")
app.include_router(admin.router, prefix="/admin")
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")


@app.get("/")
async def read_root():
    return {"message": "Welcome to UniverseLM, the future of AI"}


@app.get("/gatekeep")
async def gatekeeping_test(
    kinde_client: KindeApiClient = Depends(clients.get_kinde_client),
):
    return "You have entered the gate"


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response["message"].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)
