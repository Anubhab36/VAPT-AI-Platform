import sqlite3


DATABASE_NAME = "database/vapt_platform.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            scan_id TEXT,

            target TEXT,

            status TEXT,

            timestamp TEXT,

            duration REAL,

            total_findings INTEGER,

            risk_score REAL,

            ai_summary TEXT
        )
    """)

    connection.commit()

    connection.close()

def save_scan_to_db(scan_data):

    connection = get_connection()

    cursor = connection.cursor()

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

    cursor.execute("""
        INSERT INTO scans (
            scan_id,
            target,
            status,
            timestamp,
            duration,
            total_findings,
            risk_score,
            ai_summary
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        scan_data.get("scan_id"),

        scan_data.get("target"),

        scan_data.get("status"),

        scan_data.get("timestamp"),

        scan_data.get(
            "duration_seconds"
        ),

        summary.get(
            "total_findings"
        ),

        risk_analysis.get(
            "total_risk_score"
        ),

        analysis.get(
            "ai_summary"
        )
    ))

    connection.commit()

    connection.close()

def get_all_scans():

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]

def get_recent_scans(limit=10):

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM scans

        ORDER BY id DESC

        LIMIT ?

    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]

def get_scan_analytics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM scans
    """)

    total_scans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(risk_score)
        FROM scans
    """)

    average_risk_score = (
        cursor.fetchone()[0]
    )

    cursor.execute("""
        SELECT SUM(total_findings)
        FROM scans
    """)

    total_findings = (
        cursor.fetchone()[0]
    )

    connection.close()

    return {

        "total_scans":
            total_scans,

        "average_risk_score":
            round(
                average_risk_score or 0,
                2
            ),

        "total_findings":
            total_findings or 0
    }