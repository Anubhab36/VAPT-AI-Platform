import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from utils.logger import logger
from vapt_adk.agent import root_agent


APP_NAME = "vapt-ai"

USER_ID = "vapt-user"


session_service = InMemorySessionService()


runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=2,
        min=2,
        max=10
    ),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
async def ask_agent(message: str):

    logger.info(
        f"Starting AI Agent session."
    )

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=str(uuid.uuid4())
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=message
            )
        ]
    )

    final_response = None

    async for event in runner.run_async(

        user_id=USER_ID,

        session_id=session.id,

        new_message=content

    ):

        if not event.content:
            continue

        if not event.content.parts:
            continue

        if event.is_final_response():

            part = event.content.parts[0]

            if hasattr(part, "text"):

                final_response = part.text

    if final_response is None:

        raise RuntimeError(
            "The AI agent did not return a response."
        )

    logger.info(
        "AI Agent completed successfully."
    )

    return final_response