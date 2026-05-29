import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_httpx(subdomains):

    if not subdomains:

        return []

    try:

        command = [
            "httpx",
            "-silent"
        ]

        logger.info(
            f"Executing command: "
            f"{' '.join(command)}"
        )

        process = subprocess.run(

            command,

            input="\n".join(subdomains),

            capture_output=True,

            text=True,

            timeout=COMMAND_TIMEOUT
        )

        output = process.stdout.strip()

        if not output:

            return []

        live_hosts = output.splitlines()

        logger.info(
            "Command executed successfully"
        )

        return live_hosts

    except subprocess.TimeoutExpired:

        logger.error(
            "Command timed out"
        )

        return []

    except Exception as error:

        logger.error(
            f"HTTPX failed: {error}"
        )

        return []