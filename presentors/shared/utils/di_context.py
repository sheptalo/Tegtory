from functools import wraps
from inspect import signature


def with_context(ctx_cls):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            params = signature(ctx_cls).parameters

            values = {}
            for name, param in params.items():
                if name in kwargs.keys():
                    values[name] = kwargs.pop(name)

            ctx = ctx_cls(**values)
            return await func(*args, ctx, **kwargs)

        return wrapper

    return decorator
