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
    create_task,
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

from utils.storage_manager import (
    initialize_storage
)

from utils.target_validator import (
    validate_target
)

from vapt_adk.runner import (
    ask_agent
)

app = FastAPI(
    title=APP_NAME
)

templates = Jinja2Templates(
    directory="templates"
)

initialize_database()

initialize_storage()

logger.info(
    f"{APP_NAME} starting..."
)


class ReconRequest(BaseModel):
    target: str


class AgentRequest(BaseModel):
    message: str


@app.get("/")
def home():

    return {
        "message": "VAPT AI Platform Running"
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

    scans = get_recent_scans(limit)

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

    valid, result = validate_target(
        request.target
    )

    if not valid:

        return {

            "status": "error",

            "message": result
        }

    request.target = result

    scan_id = str(
        uuid.uuid4()
    )

    task_id = create_task(
        scan_id,
        request.target
    )

    asyncio.create_task(

        run_async_task(
            scan_id,
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

@app.post("/agent")
async def agent_chat(

    request: AgentRequest,

    authorized: bool = Depends(
        verify_api_key
    )
):
    """
    AI-powered cybersecurity assistant.

    Accepts a natural language request,
    invokes the Google ADK Agent,
    and returns a professional
    security assessment.
    """

    try:

        if not request.message.strip():

            return {

                "status": "error",

                "message":
                    "Message cannot be empty."
            }

        logger.info(
            f"Agent request: {request.message}"
        )

        response = await ask_agent(
            request.message
        )

        if response is None:

            logger.warning(
                "Agent returned no response."
            )

            return {

                "status": "error",

                "message":
                    "The AI agent did not return a response."
            }

        logger.info(
            "Agent completed successfully."
        )

        return {

            "status": "success",

            "response": response
        }

    except Exception as error:

        logger.exception(
            "Agent execution failed."
        )

        error_message = str(error)

        # ----------------------------
        # Gemini quota exceeded
        # ----------------------------

        if (
            "RESOURCE_EXHAUSTED" in error_message
            or "429" in error_message
        ):

            return {

                "status": "error",

                "message":
                    "Gemini API quota exceeded. Please wait for the quota to reset or use a Google AI project with available quota.",

                "details":
                    error_message
            }

        # ----------------------------
        # Gemini temporarily unavailable
        # ----------------------------

        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            return {

                "status": "error",

                "message":
                    "The Gemini AI service is temporarily unavailable. Please try again shortly.",

                "details":
                    error_message
            }

        # ----------------------------
        # Timeout
        # ----------------------------

        if (
            "timeout" in error_message.lower()
        ):

            return {

                "status": "error",

                "message":
                    "The AI request timed out. Please try again.",

                "details":
                    error_message
            }

        # ----------------------------
        # Generic error
        # ----------------------------

        return {

            "status": "error",

            "message":
                "Unexpected error while processing your request.",

            "details":
                error_message
        }