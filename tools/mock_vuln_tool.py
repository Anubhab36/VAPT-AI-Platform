def run_mock_vulnerability_scan(target):

    findings = []

    if "http" in target or "." in target:

        findings.append({
            "name": "Exposed Web Service",
            "severity": "medium",
            "description": "Web service exposed to internet"
        })

        findings.append({
            "name": "Potential Missing Security Headers",
            "severity": "low",
            "description": "Security headers may be missing"
        })

    return findings