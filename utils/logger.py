import logging

from config.settings import (
    DEBUG
)


LOG_LEVEL = (

    logging.DEBUG

    if DEBUG == "True"

    else logging.INFO
)


logging.basicConfig(

    level=LOG_LEVEL,

    format=(

        "%(asctime)s - "

        "%(levelname)s - "

        "%(message)s"
    )
)


logger = logging.getLogger(
    "vapt-ai-platform"
)