from pydantic import BaseModel, Field


class Lore(BaseModel):
    lore_text: str
    about_chunk: str


class Belonging(BaseModel):
    content: str
    owner: str
