from collections.abc import Callable
from typing import Any

from dishka import AsyncContainer, FromDishka
from dishka.integrations.base import wrap_injection

from domain.events import EventBus, EventType


def inject(is_async: bool = True) -> Callable:
    def decorator(func: Callable) -> Any:
        def container_getter(*_args: tuple, **_kwargs: dict) -> AsyncContainer:
            return container

        from .di import container

        return wrap_injection(
            func=func,
            container_getter=container_getter,
            is_async=is_async,
        )

    return decorator


_pending_subscriptions = []


def on_event(event_name: EventType) -> Callable:
    def decorator(func: Callable) -> Callable:
        _pending_subscriptions.append((event_name, func))
        return func

    return decorator


@inject(is_async=True)
async def subscribe_all(event_bus: FromDishka[EventBus]) -> None:
    for event_name, func in _pending_subscriptions:
        event_bus.subscribe(func, event_name)
