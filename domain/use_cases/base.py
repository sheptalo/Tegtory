from functools import wraps
from types import MethodType
from typing import Any, Callable

from common.exceptions import AppException

from ..events.eventbus import EventBus
from ..results import Failure, Success


class DependencyRequired:
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
        async def wrapper(*args: tuple, **kwargs: dict) -> Success | Failure:
            try:
                return Success(data=await obj(*args, **kwargs))
            except AppException as e:
                return Failure(reason=e.message)

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
