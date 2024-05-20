from typing import List, Set, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field


class LogicMode(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def __str__(self) -> str:
        return self.name

    def parse_str(s: str):
        if s == "AND":
            return LogicMode.AND
        elif s == "OR":
            return LogicMode.OR
        elif s == "XOR":
            return LogicMode.XOR

        # If nothing else, return None
        return None
