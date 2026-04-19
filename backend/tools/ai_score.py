from tools.live_logger import push_log
import time


def calculate_real_score(state):

    push_log("🤖 AI: Computing REAL performance metrics...")

    state["end_time"] = time.time()

    duration = state["end_time"] - state.get("start_time", state["end_time"])

    failures = len(state.get("failures", []))
    fixes = len(state.get("fixes", []))
    iteration = state.get("iteration", 1)
    status = state.get("status", "FAILED")

    # ⚡ REAL SPEED SCORE (based on execution time)
    speed_score = max(0, int(100 - duration))

    # 🔁 REAL STABILITY (retry based)
    stability_score = max(0, 100 - (iteration * 15))

    # 🛠 REAL FIX EFFICIENCY
    fix_efficiency = 100 if failures == 0 else int((fixes / failures) * 100)

    # 🧪 TEST HEALTH (real cicd result)
    test_health = 100 if status == "PASSED" else 0

    score_data = {
        "execution_time": round(duration, 2),
        "speed_score": speed_score,
        "stability_score": stability_score,
        "fix_efficiency": fix_efficiency,
        "test_health": test_health
    }

    push_log(f"🤖 REAL SCORE → {score_data}")

    return score_data
