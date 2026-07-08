from utils.logger import logger

from vapt_adk.orchestrator import (
    orchestrator
)

from vapt_adk.agent_memory import (
    agent_memory
)

from vapt_adk.tools.subfinder_tool import (
    run_subfinder
)

from vapt_adk.tools.httpx_tool import (
    run_httpx
)

from vapt_adk.tools.nmap_tool import (
    run_nmap
)

from vapt_adk.tools.vuln_tool import (
    run_vulnerability_scan
)

from vapt_adk.tools.analysis_tool import (
    analyze_results
)


class Planner:

    """
    Agent planner responsible for
    orchestrating tool execution.
    """

    def execute_scan(

        self,

        scan_id,

        target

    ):

        logger.info(
            f"Planning scan for {target}"
        )

        # --------------------------
        # Step 1
        # --------------------------

        subfinder_result = orchestrator.execute(

            scan_id,

            "subfinder",

            run_subfinder,

            target

        )

        subdomains = subfinder_result.get(
            "data",
            []
        )

        # --------------------------
        # Step 2
        # --------------------------

        httpx_result = orchestrator.execute(

            scan_id,

            "httpx",

            run_httpx,

            subdomains

        )

        live_hosts = httpx_result.get(
            "data",
            []
        )

        # --------------------------
        # Step 3
        # --------------------------

        nmap_result = orchestrator.execute(

            scan_id,

            "nmap",

            run_nmap,

            target

        )

        # --------------------------
        # Step 4
        # --------------------------

        vulnerability_result = orchestrator.execute(

            scan_id,

            "mock_vulnerability_scan",

            run_vulnerability_scan,

            target

        )

        # --------------------------
        # Step 5
        # --------------------------

        analysis = analyze_results({

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

        return {

            "tool_results": {

                "subfinder":
                    subfinder_result,

                "httpx":
                    httpx_result,

                "nmap":
                    nmap_result,

                "vulnerability":
                    vulnerability_result

            },

            "analysis":
                analysis,

            "memory":
                agent_memory.all()

        }


planner = Planner()