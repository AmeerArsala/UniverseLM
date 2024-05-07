from pydantic import BaseModel, Field


class Chunk(BaseModel):
    name: str
    profile: str
    community_id: int
    parent_chunk: str

    def wrap_result(row: tuple):
        columns = list(Chunk.schema()["properties"].keys())
        values = list(row)

        cls_dict = {col: val for (col, val) in zip(columns, values)}

        return Chunk(**cls_dict)


class User(BaseModel):
    email: str
    chunk_name: str
