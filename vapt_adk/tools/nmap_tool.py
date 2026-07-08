from tools.nmap_tool import run_nmap as execute_nmap


def run_nmap(target: str):
    """
    Executes Nmap.

    Returns standardized results.
    """

    return execute_nmap(target)
