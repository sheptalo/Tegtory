from functools import wraps
from inspect import signature
from typing import Any, Callable, Type


def with_context(ctx_cls: Type) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: tuple, **kwargs: dict) -> Any:
            params = signature(ctx_cls).parameters

            values = {}
            for name, _ in params.items():
                if name in kwargs.keys():
                    values[name] = kwargs.pop(name)

            ctx = ctx_cls(**values)
            return await func(*args, ctx, **kwargs)

        return wrapper

    return decorator
