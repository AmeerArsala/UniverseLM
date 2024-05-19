from typing import List, Dict
from pydantic import BaseModel, Field


class Community(BaseModel):
    id: int
    name: str
