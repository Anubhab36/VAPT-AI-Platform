from tools.mock_vuln_tool import (
    run_mock_vulnerability_scan as execute_scan
)


def run_vulnerability_scan(target: str):
    """
    Executes vulnerability scan.

    Returns standardized results.
    """

    return execute_scan(target)
