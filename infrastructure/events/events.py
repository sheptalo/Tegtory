from typing import Any

from dishka import FromDishka

from domain.events import EventBus
from domain.use_cases.base import EventBased
from infrastructure.di import container
from infrastructure.injectors import inject
from infrastructure.utils import get_children


@inject(is_async=True)
async def register_events(event_bus: FromDishka[EventBus]) -> None:
    events = get_subscribed_events(EventBased)

    for cls, subscribers in events:
        instance = await container.get(cls)
        for sub in subscribers:
            event_bus.subscribe(getattr(instance, sub.__name__), sub.__event__)


def get_subscribed_events(klass: type[EventBased]) -> list[list[Any]]:
    events = []
    for cls in get_children(klass):
        events.append([cls, cls.get_subscribers()])

    return events
