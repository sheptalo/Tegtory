from .event_types import EventType


def on_event(event: EventType):
    def decorator(func):
        func.__event__ = event
        return func

    return decorator
