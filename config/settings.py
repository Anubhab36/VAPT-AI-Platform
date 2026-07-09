import os

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv(
    "API_KEY"
)

APP_NAME = os.getenv(
    "APP_NAME"
)

DEBUG = os.getenv(
    "DEBUG"
)

COMMAND_TIMEOUT = int(
    os.getenv(
        "COMMAND_TIMEOUT",
        30
    )
)

NUCLEI_TIMEOUT = int(
    os.getenv(
        "NUCLEI_TIMEOUT",
        600
    )
)