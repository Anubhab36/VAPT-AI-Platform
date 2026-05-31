from pathlib import Path
import json

def get_latest_scan() -> str:
    """
    Returns latest scan result as formatted JSON string.
    """

    current_dir = Path(__file__).resolve().parent
    scan_file = current_dir.parent.parent / "storage" / "scans.json"

    if not scan_file.exists():
        return f"ERROR: scans.json not found at {scan_file}"

    try:
        with open(scan_file, "r") as f:
            scans = json.load(f)

        if not scans:
            return "ERROR: No scans available"

        return json.dumps(scans[-1], indent=2)

    except Exception as e:
        return f"ERROR: {str(e)}"