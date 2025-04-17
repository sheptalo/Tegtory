from .event_types import EventType


def on_event(*events: tuple[EventType]):
    def decorator(func):
        func.__subscribed_events__ = events
        return func

    return decorator
