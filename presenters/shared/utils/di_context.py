from collections.abc import Callable
from functools import wraps
from inspect import signature
from typing import Any


def with_context(ctx_cls: type) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any:
            params = signature(ctx_cls).parameters

            values = {}
            for name in params:
                if name in kwargs:
                    values[name] = kwargs.pop(name)

            ctx = ctx_cls(**values)
            return await func(*args, ctx, **kwargs)

        return wrapper

    return decorator
