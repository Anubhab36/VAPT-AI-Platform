from analysis.risk_engine import (
    calculate_risk_score
)

from analysis.ai_summary import (
    generate_ai_summary
)

from analysis.recommendation_engine import (
    generate_recommendations
)


def analyze_recon_data(scan_data):

    findings = []

    results = scan_data.get(
        "results",
        {}
    )

    nmap_results = results.get(
        "nmap_results",
        []
    )

    vulnerability_results = results.get(
        "vulnerability_results",
        []
    )

    live_hosts = results.get(
        "live_hosts",
        []
    )

    subdomains = results.get(
        "subdomains",
        []
    )

    for port in nmap_results:

        service = port.get(
            "service",
            ""
        )

        if service == "http":

            findings.append({
                "type": "web_service",
                "severity": "info",
                "description": (
                    "HTTP service detected"
                ),
                "port": port.get("port")
            })

        elif service == "https":

            findings.append({
                "type": "secure_web_service",
                "severity": "info",
                "description": (
                    "HTTPS service detected"
                ),
                "port": port.get("port")
            })

        elif service == "ssh":

            findings.append({
                "type": "remote_access_service",
                "severity": "medium",
                "description": (
                    "SSH service exposed"
                ),
                "port": port.get("port")
            })

    for vuln in vulnerability_results:

        findings.append({
            "type": (
                "potential_vulnerability"
            ),
            "severity": vuln.get(
                "severity"
            ),
            "description": vuln.get(
                "description"
            )
        })

    risk_analysis = (
        calculate_risk_score(
            findings
        )
    )

    summary = {
        "total_subdomains": len(
            subdomains
        ),

        "total_live_hosts": len(
            live_hosts
        ),

        "total_open_ports": len(
            nmap_results
        ),

        "total_findings": len(
            findings
        )
    }

    ai_summary = generate_ai_summary(
        findings,
        risk_analysis,
        summary
    )

    recommendations = (
        generate_recommendations(
            findings
        )
    )

    return {
        "summary": summary,

        "risk_analysis": (
            risk_analysis
        ),

        "ai_summary": ai_summary,

        "recommendations": (
            recommendations
        ),

        "findings": findings
    }