import os
from typing import Union, Optional, List, Dict

from fastapi import FastAPI, Depends, HTTPException, status, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


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


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# uvicorn main:api --reload
def start():
    uvicorn.run("main:api", reload=True)


if __name__ == "__main__":
    start()
