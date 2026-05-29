import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_subfinder(target):

    try:

        command = [
            "subfinder",
            "-silent",
            "-timeout",
            "5",
            "-d",
            target
        ]

        logger.info(
            f"Executing command: "
            f"{' '.join(command)}"
        )

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            timeout=COMMAND_TIMEOUT
        )

        output = result.stdout.strip()

        if not output:

            return []

        subdomains = output.splitlines()

        logger.info(
            "Command executed successfully"
        )

        return subdomains

    except subprocess.TimeoutExpired:

        logger.error(
            "Command timed out"
        )

        return []

    except Exception as error:

        logger.error(
            f"Subfinder failed: {error}"
        )

        return []