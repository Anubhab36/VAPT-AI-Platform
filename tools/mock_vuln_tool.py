from utils.logger import logger


def run_mock_vulnerability_scan(target):
    """
    Mock vulnerability scanner.

    Returns a standardized response object so that
    it is consistent with every other tool.
    """

    try:

        findings = []

        if "http" in target or "." in target:

            findings.append({

                "name":
                    "Exposed Web Service",

                "severity":
                    "medium",

                "description":
                    "Web service exposed to internet"
            })

            findings.append({

                "name":
                    "Potential Missing Security Headers",

                "severity":
                    "low",

                "description":
                    "Security headers may be missing"
            })

        logger.info(
            f"Mock vulnerability scan generated "
            f"{len(findings)} findings."
        )

        return {

            "success": True,

            "tool": "mock_vulnerability_scan",

            "target": target,

            "data": findings,

            "error": None
        }

    except Exception as error:

        logger.exception(
            "Mock vulnerability scan failed."
        )

        return {

            "success": False,

            "tool": "mock_vulnerability_scan",

            "target": target,

            "data": [],

            "error": str(error)
        }