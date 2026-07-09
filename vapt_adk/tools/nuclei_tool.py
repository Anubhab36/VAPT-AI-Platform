from tools.nuclei_tool import (
    run_nuclei as execute_nuclei
)


def run_nuclei(target: str):
    """
    Executes Nuclei.

    Returns standardized results.
    """

    return execute_nuclei(target)