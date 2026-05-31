from google.adk.agents.llm_agent import Agent
from tools.recon_tool import get_latest_scan

root_agent = Agent(
    model="gemini-2.5-flash",
    name="vapt_analysis_agent",
    description="AI-powered VAPT analysis agent",
    instruction="""
You are a senior cybersecurity analyst.

IMPORTANT:
If the user asks about the latest scan, scan results,
recent findings, vulnerabilities, risk score,
or asks you to analyze a scan,
you MUST call the tool get_latest_scan.

After retrieving the scan:

1. Analyze attack surface.
2. Assess risk level.
3. Identify findings.
4. Generate executive summary.
5. Generate remediation recommendations.

Always use the tool when scan data is requested.
""",
    tools=[get_latest_scan]
)