import json

STORAGE_FILE = "storage/scans.json"

def load_scans():

    with open(STORAGE_FILE, "r") as file:

        return json.load(file)

def save_scan(scan_data):

    scans = load_scans()

    scans.append(scan_data)

    with open(STORAGE_FILE, "w") as file:

        json.dump(scans, file, indent=4)