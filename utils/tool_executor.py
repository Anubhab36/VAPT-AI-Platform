import subprocess

from config.settings import SCAN_TIMEOUT

from utils.logger import logger


def execute_tool(command):

    try:

        logger.info(f"Executing command: {' '.join(command)}")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=SCAN_TIMEOUT
        )

        logger.info("Command executed successfully")

        return result.stdout

    except subprocess.TimeoutExpired:

        logger.error("Command timed out")

        return ""

    except Exception as error:

        logger.error(f"Tool execution failed: {error}")

        return ""