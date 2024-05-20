from fastapi import APIRouter, Depends, Request
from app.core import auth


router = APIRouter(dependencies=[Depends(auth.get_api_key)])
