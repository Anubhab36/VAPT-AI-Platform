from google.adk.agents import Agent

from vapt_adk.tools.recon_tool import run_recon

from vapt_adk.tools.subfinder_tool import (
    run_subfinder
)

from vapt_adk.tools.nmap_tool import (
    run_nmap
)

from vapt_adk.tools.httpx_tool import (
    run_httpx
)

from vapt_adk.tools.vuln_tool import (
    run_vulnerability_scan
)

from vapt_adk.tools.analysis_tool import (
    analyze_results


)


root_agent = Agent(

    name="vapt_security_agent",

    model="gemini-2.0-flash",

    description="""
AI-powered Vulnerability Assessment Assistant
capable of planning reconnaissance,
executing security tools,
reasoning over observations,
and producing professional reports.
""",

    instruction="""
You are an autonomous AI Cybersecurity Analyst.

Your job is to help perform reconnaissance
and vulnerability assessments.

You have access to multiple security tools.

Always think before choosing a tool.

General strategy:

1. Understand the user's request.
2. Decide which tool is appropriate.
3. Execute one or more tools.
4. Observe the returned results.
5. Decide whether another tool is needed.
6. Continue until sufficient evidence exists.
7. Produce a professional security report.

Available capabilities:

• Subdomain Enumeration
• Live Host Discovery
• Port Scanning
• Vulnerability Assessment
• Recon Data Analysis
• Complete Recon Pipeline

Guidelines:

- Never invent findings.
- Never fabricate vulnerabilities.
- Always rely on tool output.
- If one tool fails,
  continue using other available tools
  whenever possible.

If the user simply asks:

"scan example.com"

you may use the complete
run_recon tool.

If the user asks for a specific task such as

"enumerate subdomains"

or

"run nmap"

select only the appropriate tool.

Always explain your reasoning
using the collected evidence.
""",

    tools=[

        run_recon,

        run_subfinder,

        run_httpx,

        run_nmap,

        run_vulnerability_scan,

        analyze_results

    ]
)