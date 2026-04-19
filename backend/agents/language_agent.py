import os
from tools.live_logger import push_log


def detect_languages(repo_path):

    push_log("[Language Agent] Detecting project stack...")

    detected = {
        "python": False,
        "node": False,
        "docker": False,
        "multi": False
    }

    total_files = 0

    # 🔥 DEEP WALK (REAL FIX)
    for root, dirs, files in os.walk(repo_path):

        for file in files:

            total_files += 1

            fname = file.lower()

            # 🐍 PYTHON
            if fname.endswith(".py") or fname == "requirements.txt":
                detected["python"] = True

            # 🟩 NODE
            if fname.endswith(".js") or fname.endswith(".ts") or fname == "package.json":
                detected["node"] = True

            # 🐳 DOCKER
            if fname == "dockerfile":
                detected["docker"] = True

    # MULTI STACK CHECK
    if detected["python"] and detected["node"]:
        detected["multi"] = True

    push_log(f"[Language Agent] Files scanned: {total_files}")
    push_log(f"[Language Agent] Detected Stack → {detected}")

    return detected
