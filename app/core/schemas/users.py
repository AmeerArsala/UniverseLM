from typing import List, Dict
from pydantic import BaseModel, Field
from enum import IntEnum


class UserDetails(BaseModel):
    given_name: str
    id: str
    family_name: str
    email: str
    picture: str  # a link to the image


class TierPlan(IntEnum):
    FREE_TIER = 1
    PRO_TIER = 2
    SCALE_TIER = 3
    ADMIN_TIER = 4
    ALMIGHTY_TIER = 9001
