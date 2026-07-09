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

TOOL_REGISTRY = {

    "subfinder": {

        "function": run_subfinder,

        "description":
            "Discover subdomains of a target."
    },

    "httpx": {

        "function": run_httpx,

        "description":
            "Identify live hosts."
    },

    "nmap": {

        "function": run_nmap,

        "description":
            "Enumerate open ports and services."
    },

    "nuclei": {

        "function": run_nuclei,

        "description":
            "Run vulnerability assessment."
    },

    "analysis": {

        "function": analyze_results,

        "description":
            "Analyze collected reconnaissance results."
    }

}