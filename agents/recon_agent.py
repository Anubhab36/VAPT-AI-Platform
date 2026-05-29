import time

from concurrent.futures import (
    ThreadPoolExecutor
)

from tools.nmap_tool import (
    run_nmap
)

from tools.subfinder_tool import (
    run_subfinder
)

from tools.httpx_tool import (
    run_httpx
)

from tools.mock_vuln_tool import (
    run_mock_vulnerability_scan
)

from utils.helpers import (
    generate_scan_id
)

from utils.helpers import (
    get_timestamp
)

from utils.helpers import (
    calculate_duration
)

from utils.logger import logger

from utils.storage_manager import (
    save_scan
)

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

            subdomains = (
                subfinder_future.result()
            )

            nmap_results = (
                nmap_future.result()
            )

            vulnerability_results = (
                vuln_future.result()
            )

        logger.info(
            "Concurrent recon tasks completed"
        )

        live_hosts = run_httpx(
            subdomains
        )

        duration = calculate_duration(
            start_time
        )

        analysis_results = (
            analyze_recon_data({
                "results": {

                    "subdomains":
                        subdomains,

                    "live_hosts":
                        live_hosts,

                    "nmap_results":
                        nmap_results,

                    "vulnerability_results":
                        vulnerability_results
                }
            })
        )

        logger.info(
            f"Recon completed for {target}"
        )

        response = {

            "scan_id": scan_id,

            "target": target,

            "status": "completed",

            "timestamp": timestamp,

            "duration_seconds":
                duration,

            "results": {

                "subdomains":
                    subdomains,

                "live_hosts":
                    live_hosts,

                "nmap_results":
                    nmap_results,

                "vulnerability_results":
                    vulnerability_results
            },

            "analysis":
                analysis_results
        }

        update_task_status(
            scan_id,
            "completed"
        )

        save_scan(response)

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

        return response

    except Exception as error:

        duration = calculate_duration(
            start_time
        )

        update_task_status(
            scan_id,
            "failed"
        )

        logger.error(
            f"Recon failed for "
            f"{target}: {error}"
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