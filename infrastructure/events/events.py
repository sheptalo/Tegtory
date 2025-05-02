from typing import Any

from domain.interfaces import EventBus
from domain.use_cases.base import EventBased
from infrastructure.utils import get_children


async def subscribe_events() -> None:
    from ..di import container

    event_bus = await container.get(EventBus)
    events = get_subscribed_events(EventBased)

    for cls, subscribers in events:
        instance = await container.get(cls)
        for sub in subscribers:
            event_bus.subscribe(getattr(instance, sub.__name__), sub.__event__)


def get_subscribed_events(klass: type[EventBased]) -> list[list[Any]]:
    events = []
    for cls in get_children(klass):
        cls_typing: EventBased = cls
        events.append([cls_typing, cls_typing.get_subscribers()])
    print(events)
    return events
