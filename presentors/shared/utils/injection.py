import inspect


async def smart_call(func, *args, **kwargs):
    sig = inspect.signature(func)
    arg_names = set(sig.parameters)
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in arg_names}
    return await func(*args, **filtered_kwargs)
