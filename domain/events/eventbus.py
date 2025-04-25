from typing import Protocol, Self, Callable, Any

from domain.events import EventType


class EventBus(Protocol):
    _instance: Self

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance: Self = object.__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, callback: Callable, event_name: EventType) -> None:
        pass

    @classmethod
    async def emit(cls, event: EventType, *args: tuple, **kwargs: dict) -> Any:
        pass
