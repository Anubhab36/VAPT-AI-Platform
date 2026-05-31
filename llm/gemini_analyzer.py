from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def analyze_scan(scan_data: str):

    prompt = f"""
You are a senior cybersecurity analyst.

Analyze this scan result:

{scan_data}

Generate:

1. Executive Summary
2. Risk Assessment
3. Findings Analysis
4. Recommendations
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text