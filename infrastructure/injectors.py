from functools import wraps

from dishka import FromDishka
from dishka.integrations.base import wrap_injection

from domain.events import EventType
from domain.use_cases import UCFactory

from .di import container


@wraps(wrap_injection)
def inject(**params):
    def decorator(func):
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
async def subscribe_all(use_case: FromDishka[UCFactory]):
    for event_name, func in _pending_subscriptions:
        use_case.event_bus.subscribe(func, event_name)
