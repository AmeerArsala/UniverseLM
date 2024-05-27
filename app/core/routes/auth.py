from typing import Union, Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType


router = APIRouter()
