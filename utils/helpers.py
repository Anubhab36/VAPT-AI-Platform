import uuid
import time

def calculate_duration(start_time):

    return round(time.time() - start_time, 2)

from datetime import datetime

def generate_scan_id():

    return str(uuid.uuid4())

def get_timestamp():

    return datetime.now().isoformat()