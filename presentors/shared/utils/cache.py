import logging
from functools import wraps

from presentors.shared.utils.injection import smart_call

logger = logging.getLogger("cache")
_temp = {}


def cache(item, default):
    def cache_func(x):
        if x not in _temp.values():
            logger.debug(f"Caching {str(item)[:50]} with value {str(x)[:25]}")
            _temp.update({item: x})

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await smart_call(
                func,
                *args,
                cached=_temp.get(item, default),
                cache_func=cache_func,
                **kwargs,
            )

        return wrapper

    return decorator
