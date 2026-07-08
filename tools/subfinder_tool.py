import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_subfinder(target):
    """
    Executes Subfinder and returns a
    standardized response object.
    """

    command = [
        "subfinder",
        "-silent",
        "-timeout",
        "5",
        "-d",
        target
    ]

    try:

        logger.info(
            f"Executing command: {' '.join(command)}"
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT
        )

        output = result.stdout.strip()

        subdomains = (
            output.splitlines()
            if output
            else []
        )

        logger.info(
            f"Subfinder discovered "
            f"{len(subdomains)} subdomains."
        )

        return {

            "success": True,

            "tool": "subfinder",

            "target": target,

            "data": subdomains,

            "error": None
        }

    except subprocess.TimeoutExpired:

        logger.error(
            "Subfinder timed out."
        )

        return {

            "success": False,

            "tool": "subfinder",

            "target": target,

            "data": [],

            "error": "Command timed out."
        }

    except FileNotFoundError:

        logger.error(
            "Subfinder executable not found."
        )

        return {

            "success": False,

            "tool": "subfinder",

            "target": target,

            "data": [],

            "error": "Subfinder is not installed."
        }

    except Exception as error:

        logger.exception(
            "Subfinder execution failed."
        )

        return {

            "success": False,

            "tool": "subfinder",

            "target": target,

            "data": [],

            "error": str(error)
        }