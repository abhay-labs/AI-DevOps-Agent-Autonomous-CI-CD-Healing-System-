import sqlite3
from tools.live_logger import push_log

DB_PATH = "telemetry.db"


# ================= MEMORY QUERY =================

def get_known_issue_patterns():

    patterns = {}

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # ⭐ हम पिछले telemetry records पढ़ेंगे
        cursor.execute("SELECT languages, strategy, status FROM telemetry")

        rows = cursor.fetchall()

        conn.close()

        # simple frequency logic
        for row in rows:
            strategy = row[1]

            if not strategy:
                continue

            patterns[strategy] = patterns.get(strategy, 0) + 1

    except Exception:
        pass

    return patterns


# ================= DECISION ENGINE =================

def should_skip_ai_fix(failures):

    push_log("[SelfLearning] Checking telemetry memory...")

    patterns = get_known_issue_patterns()

    # 🔥 अगर agent पहले भी fixes करता रहा है
    # तो AI reasoning skip कर सकता है
    if patterns.get("python_strategy", 0) >= 3:
        push_log("[SelfLearning] Known pattern detected → fast auto-fix mode")
        return True

    return False
