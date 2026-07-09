import json
import subprocess

from utils.logger import logger
from config.settings import NUCLEI_TIMEOUT


def run_nuclei(target):

    """
    Executes a Nuclei vulnerability scan.

    Returns a standardized response.
    """

    command = [
        "nuclei",
        "-target",
        target,
        "-silent",
        "-jsonl"
    ]

    try:

        logger.info(
            f"Executing: {' '.join(command)}"
        )

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=NUCLEI_TIMEOUT
        )

        findings = []

        for line in process.stdout.splitlines():

            if not line.strip():
                continue

            try:
                findings.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:

                logger.warning(
                    "Invalid JSON returned by nuclei."
                )

        if process.returncode not in [0]:

            logger.error(
                process.stderr
            )

        return {

            "success": True,

            "tool": "nuclei",

            "target": target,

            "count": len(findings),

            "data": findings,

            "error": None

        }

    except subprocess.TimeoutExpired:

        logger.error(
            "Nuclei scan timed out."
        )

        return {

            "success": False,

            "tool": "nuclei",

            "target": target,

            "count": 0,

            "data": [],

            "error": "Timeout"

        }

    except Exception as error:

        logger.exception(
            "Nuclei execution failed."
        )

        return {

            "success": False,

            "tool": "nuclei",

            "target": target,

            "count": 0,

            "data": [],

            "error": str(error)

        }