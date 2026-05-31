task_registry = {}


def create_task(scan_id, target):

    task_registry[scan_id] = {
        "target": target,
        "status": "queued"
    }

    return scan_id


def update_task_status(scan_id, status):

    if scan_id in task_registry:

        task_registry[scan_id]["status"] = status


def get_all_tasks():

    return task_registry


def get_task(scan_id):

    return task_registry.get(scan_id)