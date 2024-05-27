from fastapi import APIRouter, Depends, Request
from app.core import api_auth


router = APIRouter(dependencies=[Depends(api_auth.get_api_key)])
