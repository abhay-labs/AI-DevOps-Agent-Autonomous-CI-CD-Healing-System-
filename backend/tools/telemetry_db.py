import sqlite3
import time
import json
from tools.live_logger import push_log

DB_PATH = "telemetry.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_url TEXT,
            languages TEXT,
            strategy TEXT,
            execution_time REAL,
            failures INTEGER,
            fixes INTEGER,
            iteration INTEGER,
            status TEXT,
            timestamp REAL
        )
    """)

    conn.commit()
    conn.close()


def save_telemetry(state):

    push_log("🤖 AI: Saving telemetry to database...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO telemetry (
            repo_url,
            languages,
            strategy,
            execution_time,
            failures,
            fixes,
            iteration,
            status,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        state.get("repo_url"),
        json.dumps(state.get("languages", {})),
        state.get("strategy"),
        state.get("score", {}).get("execution_time", 0),
        len(state.get("failures", [])),
        len(state.get("fixes", [])),
        state.get("iteration", 1),
        state.get("status"),
        time.time()
    ))

    conn.commit()
    conn.close()

    push_log("🤖 AI: Telemetry stored successfully")
