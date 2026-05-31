import asyncio
import uuid

from fastapi import FastAPI
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse

from fastapi.templating import (
    Jinja2Templates
)

from pydantic import BaseModel

from agents.recon_agent import (
    recon_agent
)

from utils.task_manager import (
    create_task
)

from utils.task_manager import (
    get_all_tasks
)

from utils.async_executor import (
    run_async_task
)

from security.auth import (
    verify_api_key
)

from database.db_manager import (
    initialize_database,
    get_all_scans,
    get_recent_scans,
    get_scan_analytics
)

from config.settings import (
    APP_NAME
)

from utils.logger import (
    logger
)

from utils.cache_manager import (
    get_cache,
    set_cache,
    cache_exists
)

app = FastAPI(
    title=APP_NAME
)

templates = Jinja2Templates(
    directory="templates"
)

initialize_database()

logger.info(
    f"{APP_NAME} starting..."
)


class ReconRequest(BaseModel):
    target: str


@app.get("/")
def home():

    return {
        "message": (
            "VAPT AI Platform Running"
        )
    }


@app.get("/tasks")
def get_tasks(

    authorized: bool = Depends(
        verify_api_key
    )
):

    return {
        "tasks": get_all_tasks()
    }


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(request: Request):

    scans = get_all_scans()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "scans": scans
        }
    )


@app.get("/history")
def scan_history(

    limit: int = 10,

    authorized: bool = Depends(
        verify_api_key
    )
):

    scans = get_recent_scans(
        limit
    )

    return {
        "history": scans
    }


@app.get("/analytics")
def analytics(

    authorized: bool = Depends(
        verify_api_key
    )
):

    cache_key = "analytics_data"

    if cache_exists(cache_key):

        return {
            "source": "cache",
            "data": get_cache(
                cache_key
            )
        }

    analytics_data = (
        get_scan_analytics()
    )

    set_cache(
        cache_key,
        analytics_data
    )

    return {
        "source": "database",
        "data": analytics_data
    }


@app.post("/recon")
async def run_recon(

    request: ReconRequest,

    authorized: bool = Depends(
        verify_api_key
    )
):

    scan_id = str(
        uuid.uuid4()
    )

    task_id = create_task(
        scan_id,
        request.target
    )

    asyncio.create_task(

        run_async_task(
            recon_agent,
            request.target
        )
    )

    return {

        "message":
            "Recon task queued",

        "task_id":
            task_id,

        "scan_id":
            scan_id,

        "target":
            request.target
    }