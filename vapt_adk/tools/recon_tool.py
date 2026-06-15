from agents.recon_agent import recon_agent


def run_recon(target: str):
    """
    Executes the existing reconnaissance pipeline.

    Args:
        target (str): Target domain or IP.

    Returns:
        dict: Reconnaissance results.
    """

    return recon_agent(target)