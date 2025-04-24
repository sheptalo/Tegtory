from functools import wraps
from types import MethodType

from common.exceptions import AppException

from ..events.eventbus import EventBus


class DependencyRequired:
    pass


class SafeCall:
    def __getattribute__(self, i):
        obj = object.__getattribute__(self, i)

        return (
            obj
            if i.startswith("_") or not isinstance(obj, MethodType)
            else self._get_wrapper(obj)
        )

    @staticmethod
    def _get_wrapper(obj):
        @wraps(obj)
        async def wrapper(*args, **kwargs):
            try:
                return await obj(*args, **kwargs)
            except AppException as e:
                return e.message

        return wrapper


class EventBased(DependencyRequired):
    def __init__(self, eventbus: EventBus):
        self.event_bus = eventbus

    @classmethod
    def get_subscribers(cls):
        subs = []
        for attr in filter(
            lambda x: hasattr(getattr(cls, x), "__event__"), dir(cls)
        ):
            subs.append(getattr(cls, attr))
        return subs
