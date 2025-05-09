import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Success(Generic[T]):
    data: T


@dataclasses.dataclass(frozen=True)
class Failure:
    reason: str
