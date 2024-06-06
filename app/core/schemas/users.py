from typing import List, Dict
from pydantic import BaseModel, Field


class UserDetails(BaseModel):
    given_name: str
    id: str
    family_name: str
    email: str
    picture: str  # a link to the image
