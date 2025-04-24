from dishka import FromDishka
from dishka.integrations.base import wrap_injection

from domain.events import EventBus, EventType


def inject(**params):
    def decorator(func):
        from .di import container

        return wrap_injection(
            func=func, container_getter=lambda __, _: container, **params
        )

    return decorator


_pending_subscriptions = []


def on_event(event_name: EventType):
    def decorator(func):
        _pending_subscriptions.append((event_name, func))
        return func

    return decorator


@inject(is_async=True)
async def subscribe_all(event_bus: FromDishka[EventBus]):
    for event_name, func in _pending_subscriptions:
        event_bus.subscribe(func, event_name)
