from functools import wraps
from types import MethodType

from common.exceptions import AppException

from ..events.eventbus import IEventBus


class BaseUseCase:
    def __init__(self, eventbus: IEventBus) -> None:
        self.event_bus = eventbus
        self._subscribe()

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

    def _subscribe(self) -> None:
        for attr in filter(
            lambda x: hasattr(getattr(self, x), "__subscribed_events__"),
            dir(self),
        ):
            func = getattr(self, attr)
            events = func.__subscribed_events__
            for event in events:
                self.event_bus.subscribe(func, event)
