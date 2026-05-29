import subprocess

from utils.logger import logger

from config.settings import (
    COMMAND_TIMEOUT
)


def run_nmap(target):

    try:

        command = [
            "nmap",
            "-F",
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

        output = result.stdout

        ports = []

        for line in output.splitlines():

            if "/tcp" in line and "open" in line:

                parts = line.split()

                ports.append({

                    "port": parts[0],

                    "state": parts[1],

                    "service": parts[2]
                })

        logger.info(
            "Command executed successfully"
        )

        return ports

    except subprocess.TimeoutExpired:

        logger.error(
            "Command timed out"
        )

        return []

    except Exception as error:

        logger.error(
            f"Nmap failed: {error}"
        )

        return []