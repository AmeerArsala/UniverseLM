from typing import List, Dict
from fastapi import APIRouter, Depends, Request
from app.core import api_auth

from app.lib import states


router = APIRouter(tags=["admin"], dependencies=[Depends(api_auth.get_admin_api_key)])


@router.post("/refresh_all_chunks")
async def refresh_all_known_chunks() -> Dict[int, List[str]]:
    return states.refresh_all_known_chunks()
