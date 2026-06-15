# AI-Powered Agentic VAPT Platform

An AI-powered Vulnerability Assessment and Penetration Testing (VAPT) platform that combines traditional cybersecurity reconnaissance tools with **Google Agent Development Kit (ADK)** and **Google Gemini AI** to perform intelligent security assessments and generate professional executive reports.

---

## 📌 Overview

Traditional vulnerability scanners produce raw technical findings that often require manual interpretation by security professionals. This project extends a conventional VAPT pipeline with an **Agentic AI Security Assistant** capable of understanding natural language requests, autonomously invoking reconnaissance tools, analyzing scan results, prioritizing risks, and generating remediation recommendations.

The platform integrates Google ADK for intelligent tool orchestration while preserving a modular FastAPI-based architecture.

---

# Features

## Traditional VAPT Features

* Network reconnaissance
* Fast port scanning using Nmap
* Subdomain enumeration using Subfinder
* Live host detection using HTTPX
* Mock vulnerability scanning
* Risk score calculation
* Recommendation engine
* Markdown report generation
* JSON report generation
* Dashboard for scan history
* SQLite database integration
* API Key authentication
* Concurrent scanning using ThreadPoolExecutor
* Scan caching
* Task management

---

## AI Features

* Google Gemini Integration
* Google Agent Development Kit (ADK)
* AI Security Assistant
* Tool Calling
* Natural language interaction
* Executive security summaries
* Risk prioritization
* Automated remediation recommendations
* AI-powered report generation

---

# Agentic Architecture

```
                           User
                             │
                             ▼
                      FastAPI Backend
                    ┌────────────────┐
                    │                │
                    ▼                ▼
               POST /recon      POST /agent
                    │                │
                    │                ▼
                    │         Google ADK Runner
                    │                │
                    │                ▼
                    │        Root AI Agent
                    │                │
                    │        Tool Invocation
                    │                │
                    └───────────────▼
                          Recon Tool
                               │
                               ▼
                     Existing Recon Agent
                               │
          ┌────────────────────────────────────┐
          │ Nmap                               │
          │ Subfinder                          │
          │ HTTPX                              │
          │ Vulnerability Scanner              │
          │ Risk Engine                        │
          │ Recommendation Engine              │
          │ Report Generator                   │
          └────────────────────────────────────┘
                               │
                               ▼
                       Gemini AI Analysis
                               │
                               ▼
                    Executive Security Report
```

---

# Project Structure

```
vapt-ai-project/

├── agents/
│   └── recon_agent.py
│
├── analysis/
│   ├── recon_analyzer.py
│   ├── recommendation_engine.py
│   ├── risk_engine.py
│   └── ai_summary.py
│
├── config/
│
├── database/
│
├── llm/
│   └── gemini_analyzer.py
│
├── reports/
│
├── security/
│
├── storage/
│
├── templates/
│
├── tools/
│   ├── httpx_tool.py
│   ├── mock_vuln_tool.py
│   ├── nmap_tool.py
│   ├── recon_tool.py
│   └── subfinder_tool.py
│
├── utils/
│
├── vapt_adk/
│   ├── agent.py
│   ├── runner.py
│   └── tools/
│       └── recon_tool.py
│
├── screenshots/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn

## Artificial Intelligence

* Google Gemini API
* Google Agent Development Kit (ADK)

## Cybersecurity

* Nmap
* HTTPX
* Subfinder

## Database

* SQLite

## Reporting

* Markdown
* JSON

## Frontend

* HTML
* CSS
* Jinja2

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/vapt-ai-project.git

cd vapt-ai-project
```

---

## Create Virtual Environment

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install External Tools

### Nmap

Ubuntu

```bash
sudo apt install nmap
```

---

### Subfinder

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

## Configure Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
API_KEY=YOUR_SECRET_API_KEY
```

---

# Running the Project

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

Swagger UI will display all available endpoints.

---

# API Endpoints

## Home

```
GET /
```

Returns platform status.

---

## Dashboard

```
GET /dashboard
```

Displays scan history.

---

## Analytics

```
GET /analytics
```

Returns platform analytics.

---

## Scan History

```
GET /history
```

Returns recent scans.

---

## Tasks

```
GET /tasks
```

Returns background task status.

---

## Traditional Recon API

```
POST /recon
```

Example

```json
{
    "target":"scanme.nmap.org"
}
```

Response

* Reconnaissance Results
* Vulnerabilities
* Risk Score
* Recommendations
* Report Paths

---

## Agentic AI Endpoint

```
POST /agent
```

Example

```json
{
    "message":"Perform a security assessment on scanme.nmap.org"
}
```

The AI Agent automatically:

* Understands the request
* Invokes the Recon Tool
* Performs reconnaissance
* Analyzes findings
* Calculates risks
* Generates recommendations
* Returns a professional executive report

---

# AI Workflow

```
Natural Language Request

↓

Google ADK Runner

↓

Google ADK Root Agent

↓

Tool Calling

↓

Recon Tool

↓

Recon Agent

↓

Nmap
Subfinder
HTTPX

↓

Risk Analysis

↓

Recommendations

↓

Gemini AI

↓

Executive Security Report
```

---

# Example AI Request

```
Perform a security assessment on scanme.nmap.org
```

Example Response

```
Executive Summary

Attack Surface

Open Services

Risk Assessment

Security Findings

Recommended Remediation

Overall Security Posture
```

---

# Screenshots

Include screenshots of:

* Dashboard
* Swagger API
* Analytics
* AI Agent Response
* Project Structure

---

# Future Improvements

* CVE Database Integration
* OWASP ZAP Integration
* Nikto Integration
* Nuclei Integration
* Docker Support
* Kubernetes Deployment
* SIEM Integration
* Threat Intelligence APIs
* Multi-Agent Collaboration
* PDF Report Generation
* Email Reporting

---

# Learning Outcomes

This project demonstrates practical implementation of:

* Vulnerability Assessment
* Penetration Testing
* FastAPI Development
* Agentic AI
* Google ADK
* Google Gemini
* Tool Calling
* Concurrent Programming
* REST API Development
* Risk Assessment
* Report Generation
* Authentication
* Database Integration

---

# Resume Description

**AI-Powered Agentic VAPT Platform | Python, FastAPI, Google ADK, Gemini AI, Nmap, SQLite**

Developed an AI-powered Vulnerability Assessment and Penetration Testing platform integrating Google Agent Development Kit (ADK) with FastAPI. Built an autonomous cybersecurity assistant capable of interpreting natural language requests, orchestrating reconnaissance tools, performing AI-assisted security analysis, calculating risk scores, and generating executive security reports. Implemented concurrent scanning, authentication, dashboard visualization, report generation, caching, and SQLite-based scan management.

---

# License

This project is developed for educational and research purposes.
