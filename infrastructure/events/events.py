from dishka import FromDishka

from domain.events import IEventBus
from domain.use_cases.base import EventBased
from infrastructure.injectors import inject


@inject(is_async=True)
async def register_events(event_bus: FromDishka[IEventBus]):
    subs = get_subscribed_events(EventBased.__subclasses__())

    for sub in subs:
        event_bus.subscribe(sub, sub.__event__)


def get_subscribed_events(subclasses) -> list[callable]:
    events = []
    for klass in subclasses:
        events.extend(klass.get_subscribers())
        events.extend(get_subscribed_events(klass.__subclasses__()))
    return events
