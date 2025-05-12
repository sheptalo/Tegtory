from collections.abc import Callable
from functools import wraps
from types import MethodType
from typing import Any, Protocol

from common.exceptions import AppError
from domain.interfaces.eventbus import EventBus


class DependencyRequired(Protocol):
    pass


class SafeCall:
    def __getattribute__(self, i: str) -> Any:
        obj = object.__getattribute__(self, i)
        return (
            obj if not isinstance(obj, MethodType) else self._get_wrapper(obj)
        )

    @staticmethod
    def _get_wrapper(obj: Callable) -> Callable:
        @wraps(obj)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any:
            try:
                return await obj(*args, **kwargs)
            except AppError as e:
                return e.message

        return wrapper


class EventBased(DependencyRequired):
    def __init__(self, eventbus: EventBus) -> None:
        self.event_bus = eventbus

    @classmethod
    def get_subscribers(cls) -> list[Callable]:
        subs = []
        for attr in filter(
            lambda x: hasattr(getattr(cls, x), "__event__"), dir(cls)
        ):
            subs.append(getattr(cls, attr))
        return subs
