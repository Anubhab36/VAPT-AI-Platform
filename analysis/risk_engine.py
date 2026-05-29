SEVERITY_SCORES = {
    "info": 1,
    "low": 3,
    "medium": 6,
    "high": 8,
    "critical": 10
}


def calculate_risk_score(findings):

    total_score = 0

    for finding in findings:

        severity = finding.get(
            "severity",
            "info"
        )

        score = SEVERITY_SCORES.get(
            severity,
            1
        )

        finding["risk_score"] = score

        total_score += score

    return {
        "total_risk_score": total_score,
        "average_risk_score": (
            total_score / len(findings)
            if findings else 0
        )
    }