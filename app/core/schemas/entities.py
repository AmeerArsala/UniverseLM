from pydantic import BaseModel, Field


ID_PENDING = -1


class Chunk(BaseModel):
    id: int = Field(default=ID_PENDING)
    name: str
    profile: str
    community_id: int
    parent_chunk: str

    def wrap_result(row: tuple):
        columns = list(Chunk.schema()["properties"].keys())
        values = list(row)

        cls_dict = {col: val for (col, val) in zip(columns, values)}

        return Chunk(**cls_dict)
