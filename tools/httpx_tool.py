import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_httpx(subdomains):
    """
    Executes HTTPX against discovered
    subdomains and returns a standardized
    response object.
    """

    if not subdomains:

        return {

            "success": True,

            "tool": "httpx",

            "target": None,

            "data": [],

            "error": None
        }

    command = [
        "httpx",
        "-silent"
    ]

    try:

        logger.info(
            f"Executing command: {' '.join(command)}"
        )

        process = subprocess.run(

            command,

            input="\n".join(subdomains),

            capture_output=True,

            text=True,

            timeout=COMMAND_TIMEOUT
        )

        output = process.stdout.strip()

        live_hosts = (
            output.splitlines()
            if output
            else []
        )

        logger.info(
            f"HTTPX discovered "
            f"{len(live_hosts)} live hosts."
        )

        return {

            "success": True,

            "tool": "httpx",

            "target": None,

            "data": live_hosts,

            "error": None
        }

    except subprocess.TimeoutExpired:

        logger.error(
            "HTTPX timed out."
        )

        return {

            "success": False,

            "tool": "httpx",

            "target": None,

            "data": [],

            "error": "Command timed out."
        }

    except FileNotFoundError:

        logger.error(
            "HTTPX executable not found."
        )

        return {

            "success": False,

            "tool": "httpx",

            "target": None,

            "data": [],

            "error": "HTTPX is not installed."
        }

    except Exception as error:

        logger.exception(
            "HTTPX execution failed."
        )

        return {

            "success": False,

            "tool": "httpx",

            "target": None,

            "data": [],

            "error": str(error)
        }