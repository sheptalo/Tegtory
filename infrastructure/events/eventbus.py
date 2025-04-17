import asyncio
import logging

from domain.events import IEventBus

logger = logging.getLogger("eventbus")


class MemoryEventBus(IEventBus):
    events = {}

    @classmethod
    def subscribe(cls, callback, event_name):
        logger.debug(
            f"Subscribing to event {event_name} by {callback.__name__}"
        )
        if not cls.events.get(event_name):
            cls.events[event_name] = []
        cls.events[event_name].append(callback)

    @classmethod
    async def emit(cls, event: str, *args, **kwargs):
        logger.info(
            f"Emitting event: {event} with data:\n{cls._format_dict(kwargs)}"
        )
        for callback in cls.events.get(event, []):
            logger.debug(f"Emitting callback: {callback}")

            async def wrapper():
                try:
                    await callback(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f"Exception raised: {e} while executing {callback}"
                    )

            _ = asyncio.create_task(wrapper())

    @classmethod
    def _format_dict(cls, data: dict):
        return "\n".join([f"{k} = {v}" for k, v in data.items()])
