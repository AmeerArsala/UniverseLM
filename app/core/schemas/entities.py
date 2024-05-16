from typing import List, Dict
from pydantic import BaseModel, Field

from app.constants import NULL_PARENT_CHUNK_INDICATOR
from app.lib.utils.cryptography import small_uid


ID_PENDING = -1


class Chunk(BaseModel):
    id: int = Field(default=ID_PENDING)
    name: str
    profile: str
    community_id: int
    parent_chunk: str

    # For an uploadable dict, parent_chunk must be an int id (or NULL) and `id` cannot just be a pending negative number
    def as_uploadable_dicts(chunks: List) -> List[Dict]:
        chunks_to_upload: List[Dict] = []
        chunks_names_to_ids: Dict[str, int] = {}

        # First pass: Ensure unique ids for each chunk + map names to them
        for chunk in chunks:
            uid: int = small_uid() if chunk.id == ID_PENDING else chunk.id

            # Map the name to a uid for the second pass to deal with parent_chunk
            chunks_names_to_ids[chunk.name] = uid

            # Set the uid
            chunk_dict: Dict = chunk.dict()
            chunk_dict["id"] = uid

            chunks_to_upload.append(chunk_dict)

        # Second pass: resolve parent_chunk to contain ids
        for chunk_dict in chunks_to_upload:
            parent_chunk_name: str = chunk_dict["parent_chunk"]

            # Set parent chunk id
            if parent_chunk_name == NULL_PARENT_CHUNK_INDICATOR:
                chunk_dict["parent_chunk"] = None  # NULL
            else:
                chunk_dict["parent_chunk"] = chunks_names_to_ids[parent_chunk_name]

        return chunks_to_upload

    def wrap_result(row: tuple):
        columns = list(Chunk.schema()["properties"].keys())
        values = list(row)

        # Take care of the last value (parent_chunk)
        if values[-1] is None:
            values[-1] = NULL_PARENT_CHUNK_INDICATOR

        cls_dict = {col: val for (col, val) in zip(columns, values)}

        return Chunk(**cls_dict)
