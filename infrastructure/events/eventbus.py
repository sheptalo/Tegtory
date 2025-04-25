import asyncio
import logging
from typing import Any, Callable

from domain.events import EventBus, EventType

logger = logging.getLogger("eventbus")


class MemoryEventBus(EventBus):
    events: dict[Any, list[Callable]] = {}

    @classmethod
    def subscribe(cls, callback: Callable, event_name: EventType) -> None:
        logger.debug(
            f"Subscribing to event {event_name} by {callback.__name__}"
        )
        if not cls.events.get(event_name):
            cls.events[event_name] = []
        cls.events[event_name].append(callback)

    @classmethod
    async def emit(cls, event: EventType, *args: tuple, **kwargs: dict) -> Any:
        logger.info(
            f"Emitting event: {event} with data:\n{cls._format_dict(kwargs)}"
        )
        for callback in cls.events.get(event, []):
            logger.debug(f"Emitting callback: {callback}")

            async def wrapper() -> None:
                try:
                    await callback(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"Exception raised: {e} while executing {callback}"
                    )

            _ = asyncio.create_task(wrapper())

    @classmethod
    def _format_dict(cls, data: dict) -> str:
        return "\n".join([f"{k} = {v}" for k, v in data.items()])
