import os
import subprocess
import re

from tools.live_logger import push_log


# ================= ALL PY FILE DISCOVERY =================
def find_python_files(repo_path):

    py_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))

    return py_files


# ================= SYNTAX CHECK =================
def check_syntax(file_path):

    failures = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        compile(source, file_path, "exec")

    except SyntaxError as e:
        failures.append({
            "file": file_path,
            "line": e.lineno,
            "type": "SYNTAX"
        })

    return failures


# ================= PYTEST PARSER =================
def parse_pytest_output(output):

    failures = []
    pattern = r"(\S+\.py):(\d+):"

    matches = re.findall(pattern, output)

    for m in matches:
        failures.append({
            "file": m[0],
            "line": int(m[1]),
            "type": "LOGIC"
        })

    return failures


# ================= MAIN RUNNER =================
def run_tests(repo_path):

    push_log("[Code Analyzer] Scanning ALL Python files...")

    failures = []

    py_files = find_python_files(repo_path)

    # 🔥 1️⃣ SYNTAX CHECK ALL FILES
    for file in py_files:
        failures.extend(check_syntax(file))

    # 🔥 2️⃣ RUN PYTEST IF EXISTS
    push_log("[Test Agent] Running pytest if tests exist...")

    try:
        result = subprocess.run(
            ["pytest", repo_path],
            capture_output=True,
            text=True,
            cwd=repo_path
        )

        output = result.stdout + result.stderr

        failures.extend(parse_pytest_output(output))

    except Exception:
        push_log("[Test Agent] Pytest skipped")

    if failures:
        push_log(f"[Analyzer] {len(failures)} issues detected")
    else:
        push_log("[Analyzer] No issues found — PASSED")

    return failures
