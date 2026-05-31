import os

from google import genai


def generate_ai_summary(
    findings,
    risk_analysis,
    summary
):
    """
    Generate AI-powered scan summary using Gemini.
    Falls back to rule-based summary if Gemini fails.
    """

    try:

        client = genai.Client(
            api_key=os.getenv(
                "GOOGLE_API_KEY"
            )
        )

        prompt = f"""
You are a senior cybersecurity analyst.

Analyze the following VAPT scan results.

Summary:
{summary}

Risk Analysis:
{risk_analysis}

Findings:
{findings}

Generate a professional executive summary.

Requirements:
- Maximum 250 words
- Mention overall risk level
- Mention important exposed services
- Mention attack surface concerns
- Mention remediation priorities
- Use professional cybersecurity language
"""

        response = (
            client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        )

        return response.text

    except Exception as e:

        # Fallback to old logic

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

        return " ".join(summary_lines)