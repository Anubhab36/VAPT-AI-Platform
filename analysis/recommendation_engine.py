def generate_recommendations(findings):

    recommendations = []

    for finding in findings:

        finding_type = finding.get(
            "type"
        )

        if finding_type == "remote_access_service":

            recommendations.append(
                "Restrict SSH access using firewall rules and key-based authentication."
            )

        elif finding_type == "web_service":

            recommendations.append(
                "Review exposed web services and apply proper security headers."
            )

        elif finding_type == "secure_web_service":

            recommendations.append(
                "Ensure HTTPS services use strong TLS configurations."
            )

        elif finding_type == "potential_vulnerability":

            recommendations.append(
                "Investigate the detected vulnerability and apply necessary patches."
            )

    unique_recommendations = list(
        set(recommendations)
    )

    return unique_recommendations