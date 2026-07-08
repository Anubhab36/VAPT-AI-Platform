import os

from dotenv import load_dotenv

from fastapi import Header
from fastapi import HTTPException


load_dotenv()


API_KEY = os.getenv("API_KEY")


def verify_api_key(
    x_api_key: str = Header(None)
):
    """
    Verifies the API key supplied in the
    X-API-Key request header.
    """

    if API_KEY is None:

        raise HTTPException(
            status_code=500,
            detail="API_KEY is not configured."
        )

    if x_api_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return True