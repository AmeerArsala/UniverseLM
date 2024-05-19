import anyio
from functools import wraps


def fire_and_forget(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        async with anyio.create_task_group() as group:
            group.start_soon(f, *args, **kwargs)
    return wrapper