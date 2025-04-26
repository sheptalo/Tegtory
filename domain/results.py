from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Success(BaseModel, Generic[T]):
    data: T


class Failure(BaseModel):
    reason: str
