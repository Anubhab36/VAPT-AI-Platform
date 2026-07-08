import os
import json


STORAGE_DIR = "storage"
STORAGE_FILE = os.path.join(
    STORAGE_DIR,
    "scans.json"
)


def initialize_storage():
    """
    Creates the storage directory and scans.json
    if they do not already exist.
    """

    os.makedirs(
        STORAGE_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        STORAGE_FILE
    ):

        with open(
            STORAGE_FILE,
            "w"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


def load_scans():

    initialize_storage()

    with open(
        STORAGE_FILE,
        "r"
    ) as file:

        return json.load(file)


def save_scan(scan_data):

    scans = load_scans()

    scans.append(scan_data)

    with open(
        STORAGE_FILE,
        "w"
    ) as file:

        json.dump(
            scans,
            file,
            indent=4
        )