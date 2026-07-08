import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_nmap(target):
    """
    Executes Nmap and returns a
    standardized response object.
    """

    command = [
        "nmap",
        "-F",
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

        output = result.stdout

        ports = []

        for line in output.splitlines():

            if "/tcp" in line and "open" in line:

                parts = line.split()

                if len(parts) >= 3:

                    ports.append({

                        "port": parts[0],

                        "state": parts[1],

                        "service": parts[2]
                    })

        logger.info(
            f"Nmap discovered {len(ports)} open ports."
        )

        return {

            "success": True,

            "tool": "nmap",

            "target": target,

            "data": ports,

            "error": None
        }

    except subprocess.TimeoutExpired:

        logger.error(
            "Nmap timed out."
        )

        return {

            "success": False,

            "tool": "nmap",

            "target": target,

            "data": [],

            "error": "Command timed out."
        }

    except FileNotFoundError:

        logger.error(
            "Nmap executable not found."
        )

        return {

            "success": False,

            "tool": "nmap",

            "target": target,

            "data": [],

            "error": "Nmap is not installed."
        }

    except Exception as error:

        logger.exception(
            "Nmap execution failed."
        )

        return {

            "success": False,

            "tool": "nmap",

            "target": target,

            "data": [],

            "error": str(error)
        }