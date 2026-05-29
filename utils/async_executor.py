import asyncio

from concurrent.futures import (
    ThreadPoolExecutor
)


executor = ThreadPoolExecutor(
    max_workers=5
)


async def run_async_task(
    function,
    *args
):

    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        executor,
        function,
        *args
    )

    return result