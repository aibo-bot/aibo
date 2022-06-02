import asyncio
from functools import wraps


def to_thread(func):
    @wraps(func)
    def deco(*args, **kwargs):
        return asyncio.to_thread(
            func,
            *args, **kwargs
        )

    return deco