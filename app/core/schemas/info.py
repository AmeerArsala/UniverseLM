from typing import List, Dict
from pydantic import BaseModel, Field


class Lore(BaseModel):
    lore_text: str
    about_chunks: List[str]


class Belonging(BaseModel):
    content: str
