from functools import wraps
from types import MethodType
from typing import Any, Callable

from common.exceptions import AppException

from ..events.eventbus import EventBus


class DependencyRequired:
    pass


class SafeCall:
    def __getattribute__(self, i: str) -> Any:
        obj = object.__getattribute__(self, i)

        return (
            obj
            if i.startswith("_") or not isinstance(obj, MethodType)
            else self._get_wrapper(obj)
        )

    @staticmethod
    def _get_wrapper(obj: Callable) -> Callable:
        @wraps(obj)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any | str:
            try:
                return await obj(*args, **kwargs)
            except AppException as e:
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
