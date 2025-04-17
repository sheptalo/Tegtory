from typing import Protocol


class IEventBus(Protocol):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, callback, event_name):
        pass

    @classmethod
    async def emit(cls, event: str, *args, **kwargs):
        pass
