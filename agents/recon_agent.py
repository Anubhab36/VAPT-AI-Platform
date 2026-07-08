import time

from concurrent.futures import ThreadPoolExecutor

from tools.subfinder_tool import run_subfinder
from tools.nmap_tool import run_nmap
from tools.httpx_tool import run_httpx
from tools.mock_vuln_tool import run_mock_vulnerability_scan

from utils.helpers import (
    generate_scan_id,
    get_timestamp,
    calculate_duration
)

from utils.logger import logger

from utils.storage_manager import save_scan

from utils.task_manager import (
    update_task_status
)

from utils.report_generator import (
    save_report
)

from analysis.recon_analyzer import (
    analyze_recon_data
)

from database.db_manager import (
    save_scan_to_db
)

from utils.cache_manager import (
    cache_exists,
    set_cache
)


def recon_agent(target):

    scan_id = generate_scan_id()

    cache_key = f"scan:{target}"

    if cache_exists(cache_key):

        logger.info(
            f"Using cached scan for {target}"
        )

        return

    timestamp = get_timestamp()

    start_time = time.time()

    try:

        logger.info(
            f"Running recon on {target}"
        )

        logger.info(
            "Starting concurrent recon tasks"
        )

        with ThreadPoolExecutor(
            max_workers=3
        ) as executor:

            subfinder_future = executor.submit(
                run_subfinder,
                target
            )

            nmap_future = executor.submit(
                run_nmap,
                target
            )

            vuln_future = executor.submit(
                run_mock_vulnerability_scan,
                target
            )

            subfinder_result = (
                subfinder_future.result()
            )

            nmap_result = (
                nmap_future.result()
            )

            vulnerability_result = (
                vuln_future.result()
            )

        logger.info(
            "Concurrent recon tasks completed"
        )

        subdomains = (
            subfinder_result["data"]
            if subfinder_result["success"]
            else []
        )

        live_result = run_httpx(
            subdomains
        )

        live_hosts = (
            live_result["data"]
            if live_result["success"]
            else []
        )

        duration = calculate_duration(
            start_time
        )

        analysis_results = analyze_recon_data({

            "results": {

                "subdomains":
                    subdomains,

                "live_hosts":
                    live_hosts,

                "nmap_results":
                    nmap_result["data"],

                "vulnerability_results":
                    vulnerability_result["data"]
            }
        })

        tool_status = {

            "subfinder": {
                "success": subfinder_result["success"],
                "error": subfinder_result["error"]
            },

            "nmap": {
                "success": nmap_result["success"],
                "error": nmap_result["error"]
            },

            "httpx": {
                "success": live_result["success"],
                "error": live_result["error"]
            },

            "mock_vulnerability_scan": {
                "success": vulnerability_result["success"],
                "error": vulnerability_result["error"]
            }
        }

        response = {

            "scan_id": scan_id,

            "target": target,

            "status": "completed",

            "timestamp": timestamp,

            "duration_seconds": duration,

            "tool_status": tool_status,

            "results": {

                "subdomains": subdomains,

                "live_hosts": live_hosts,

                "nmap_results":
                    nmap_result["data"],

                "vulnerability_results":
                    vulnerability_result["data"]
            },

            "analysis":
                analysis_results
        }

        update_task_status(
            scan_id,
            "completed"
        )

        save_scan(
            response
        )

        save_scan_to_db(
            response
        )

        report_files = save_report(
            response
        )

        response["reports"] = (
            report_files
        )

        set_cache(
            cache_key,
            response
        )

        logger.info(
            f"Recon completed for {target}"
        )

        return response

    except Exception as error:

        duration = calculate_duration(
            start_time
        )

        update_task_status(
            scan_id,
            "failed"
        )

        logger.exception(
            f"Recon failed for {target}"
        )

        return {

            "scan_id":
                scan_id,

            "target":
                target,

            "status":
                "failed",

            "timestamp":
                timestamp,

            "duration_seconds":
                duration,

            "error":
                str(error)
        }