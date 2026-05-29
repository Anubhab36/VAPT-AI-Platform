def generate_ai_summary(
    findings,
    risk_analysis,
    summary
):

    total_findings = summary.get(
        "total_findings",
        0
    )

    total_ports = summary.get(
        "total_open_ports",
        0
    )

    risk_score = risk_analysis.get(
        "total_risk_score",
        0
    )

    summary_lines = []

    summary_lines.append(
        f"The scan identified {total_findings} findings."
    )

    summary_lines.append(
        f"{total_ports} open ports were detected."
    )

    summary_lines.append(
        f"The overall calculated risk score is {risk_score}."
    )

    high_risk_findings = [
        finding for finding in findings
        if finding.get("severity")
        in ["high", "critical"]
    ]

    if high_risk_findings:

        summary_lines.append(
            "High-risk findings were detected."
        )

    medium_risk_findings = [
        finding for finding in findings
        if finding.get("severity") == "medium"
    ]

    if medium_risk_findings:

        summary_lines.append(
            "Medium-risk services or vulnerabilities are present."
        )

    web_services = [
        finding for finding in findings
        if finding.get("type")
        in [
            "web_service",
            "secure_web_service"
        ]
    ]

    if web_services:

        summary_lines.append(
            "Web attack surface exposure was identified."
        )

    return " ".join(summary_lines)