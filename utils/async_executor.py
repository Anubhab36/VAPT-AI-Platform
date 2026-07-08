import asyncio

from concurrent.futures import ThreadPoolExecutor

from utils.task_manager import update_task_status


executor = ThreadPoolExecutor(
    max_workers=5
)


async def run_async_task(
    scan_id,
    function,
    *args
):
    """
    Executes a task in a background thread while
    automatically updating its lifecycle.

    queued
        ↓
    running
        ↓
    completed / failed
    """

    loop = asyncio.get_running_loop()

    update_task_status(
        scan_id,
        "running"
    )

    try:

        result = await loop.run_in_executor(
            executor,
            function,
            *args
        )

        update_task_status(
            scan_id,
            "completed"
        )

        return result

    except Exception as error:

        update_task_status(
            scan_id,
            "failed"
        )

        raise error