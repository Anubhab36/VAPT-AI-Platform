import json
import os


def generate_markdown_report(scan_data):

    target = scan_data.get(
        "target"
    )

    analysis = scan_data.get(
        "analysis",
        {}
    )

    summary = analysis.get(
        "summary",
        {}
    )

    risk_analysis = analysis.get(
        "risk_analysis",
        {}
    )

    findings = analysis.get(
        "findings",
        []
    )

    ai_summary = analysis.get(
        "ai_summary",
        ""
    )

    recommendations = analysis.get(
        "recommendations",
        []
    )

    report = (
        f"# Recon Report for "
        f"{target}\n\n"
    )

    report += "## AI Summary\n\n"

    report += (
        f"{ai_summary}\n\n"
    )

    report += "## Summary\n\n"

    report += (
        f"- Total Findings: "
        f"{summary.get('total_findings')}\n"
    )

    report += (
        f"- Total Open Ports: "
        f"{summary.get('total_open_ports')}\n"
    )

    report += (
        f"- Total Live Hosts: "
        f"{summary.get('total_live_hosts')}\n"
    )

    report += (
        f"- Total Risk Score: "
        f"{risk_analysis.get('total_risk_score')}\n\n"
    )

    report += "## Findings\n\n"

    for finding in findings:

        report += (
            f"### {finding.get('type')}\n"
        )

        report += (
            f"- Severity: "
            f"{finding.get('severity')}\n"
        )

        report += (
            f"- Risk Score: "
            f"{finding.get('risk_score')}\n"
        )

        report += (
            f"- Description: "
            f"{finding.get('description')}\n\n"
        )

    report += (
        "## Recommendations\n\n"
    )

    for recommendation in recommendations:

        report += (
            f"- {recommendation}\n"
        )

    report += "\n"

    return report


def save_report(scan_data):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    scan_id = scan_data.get(
        "scan_id"
    )

    markdown_report = (
        generate_markdown_report(
            scan_data
        )
    )

    markdown_path = (
        f"reports/{scan_id}.md"
    )

    with open(
        markdown_path,
        "w"
    ) as file:

        file.write(
            markdown_report
        )

    json_path = (
        f"reports/{scan_id}.json"
    )

    with open(
        json_path,
        "w"
    ) as file:

        json.dump(
            scan_data,
            file,
            indent=4
        )

    return {
        "markdown_report":
            markdown_path,

        "json_report":
            json_path
    }