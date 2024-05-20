import os
from sys import prefix
from typing import Union, Optional, List, Dict

from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.core.routes import apotheosis, chat, functions, dataview
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


app.include_router(apotheosis.router, prefix="/apotheosis")
app.include_router(chat.router, prefix="/chat")
app.include_router(functions.router, prefix="/community")
app.include_router(dataview.router, prefix="/view")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/refresh_all_chunks")
async def refresh_all_known_chunks() -> Dict[int, List[str]]:
    return states.refresh_all_known_chunks()


# uvicorn main:app --reload
def start():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    start()
