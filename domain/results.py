from typing import Any

from pydantic import BaseModel


class Success(BaseModel):
    data: Any


class Failure(BaseModel):
    reason: str
