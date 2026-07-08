import sqlite3
import json

from datetime import datetime


DATABASE_NAME = "database/vapt_platform.db"


def get_connection():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------
    # Scan Summary Table
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Agent Context Table
    # --------------------------------------------------

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS scan_context (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            scan_id TEXT NOT NULL,

            tool_name TEXT NOT NULL,

            tool_success INTEGER NOT NULL,

            tool_output TEXT,

            tool_error TEXT,

            created_at TEXT

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

        scan_data.get(
            "scan_id"
        ),

        scan_data.get(
            "target"
        ),

        scan_data.get(
            "status"
        ),

        scan_data.get(
            "timestamp"
        ),

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

        SELECT *

        FROM scans

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


# =====================================================
# Agent Context Storage
# =====================================================

def save_tool_result(

    scan_id,

    tool_name,

    success,

    output,

    error=None

):
    """
    Stores the output produced by
    each tool execution.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO scan_context (

            scan_id,

            tool_name,

            tool_success,

            tool_output,

            tool_error,

            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?)

    """, (

        scan_id,

        tool_name,

        int(success),

        json.dumps(output),

        error,

        datetime.now().isoformat()

    ))

    connection.commit()

    connection.close()

def get_scan_context(scan_id):
    """
    Returns every tool execution
    belonging to a scan.
    """

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""

        SELECT *

        FROM scan_context

        WHERE scan_id=?

        ORDER BY id

    """, (

        scan_id,

    ))

    rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        item = dict(row)

        if item["tool_output"]:

            try:

                item["tool_output"] = json.loads(
                    item["tool_output"]
                )

            except Exception:

                pass

        results.append(item)

    return results


def get_latest_context(target):
    """
    Returns the most recent
    tool execution history
    for a target.
    """

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""

        SELECT scan_id

        FROM scans

        WHERE target=?

        ORDER BY id DESC

        LIMIT 1

    """, (

        target,

    ))

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return []

    return get_scan_context(
        row["scan_id"]
    )


def get_tool_history(
    target,
    tool_name
):
    """
    Returns historical executions
    of a specific tool
    for a target.
    """

    connection = get_connection()

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""

        SELECT
            sc.target,
            ctx.*

        FROM scan_context ctx

        JOIN scans sc

        ON ctx.scan_id = sc.scan_id

        WHERE

            sc.target = ?

            AND

            ctx.tool_name = ?

        ORDER BY ctx.id DESC

    """, (

        target,

        tool_name

    ))

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        item = dict(row)

        if item["tool_output"]:

            try:

                item["tool_output"] = json.loads(
                    item["tool_output"]
                )

            except Exception:

                pass

        history.append(item)

    return history