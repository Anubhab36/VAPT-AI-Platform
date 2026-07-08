import ipaddress
import re
from urllib.parse import urlparse


def validate_target(target: str):
    """
    Validates a scan target.

    Returns:
        (True, cleaned_target)
        (False, error_message)
    """

    target = target.strip()

    if not target:
        return False, "Target cannot be empty."

    # Remove protocol if supplied
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        target = parsed.hostname or ""

    target = target.lower()

    # Block localhost
    if target == "localhost":
        return False, "Scanning localhost is not allowed."

    # Check IP address
    try:
        ip = ipaddress.ip_address(target)

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_link_local
        ):
            return False, "Private or reserved IP addresses are not allowed."

        return True, target

    except ValueError:
        pass

    # Domain validation
    domain_pattern = (
        r"^(?!-)"
        r"[A-Za-z0-9-]{1,63}"
        r"(?<!-)"
        r"(\.[A-Za-z]{2,})+$"
    )

    if not re.fullmatch(domain_pattern, target):
        return False, "Invalid domain name."

    return True, target