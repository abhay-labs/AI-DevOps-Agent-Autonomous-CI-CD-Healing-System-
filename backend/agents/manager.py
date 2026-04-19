from agents.repo_agent import clone_repo
from agents.test_agent import run_tests
from agents.fix_agent import generate_fixes
from agents.cicd_agent import monitor_cicd
from tools.github_tools import commit_and_push
import json
import os

RESULT_PATH = "results/results.json"
RETRY_LIMIT = 5


def run_pipeline(repo_url, team, leader):

    print("Starting Agent Pipeline...")

    timeline = []
    all_fixes = []
    branch = ""
    status = "FAILED"

    try:
        # ================= CLONE REPO =================
        repo_path = clone_repo(repo_url)

        # ================= AUTO RETRY LOOP =================
        for iteration in range(1, RETRY_LIMIT + 1):

            print(f"Iteration {iteration} started")

            failures = run_tests(repo_path)

            if not failures:
                status = "PASSED"
                timeline.append({
                    "iteration": iteration,
                    "status": "PASSED"
                })
                break

            fixes = generate_fixes(failures, repo_path)
            all_fixes.extend(fixes)

            branch = commit_and_push(repo_path, fixes, team, leader)

            cicd_status = monitor_cicd(branch)

            timeline.append({
                "iteration": iteration,
                "status": cicd_status
            })

            if cicd_status == "PASSED":
                status = "PASSED"
                break

        result_data = {
            "repo": repo_url,
            "branch": branch,
            "timeline": timeline,
            "fixes": all_fixes,
            "status": status
        }

    except Exception as e:
        print("Pipeline Error:", str(e))
        result_data = {
            "repo": repo_url,
            "status": "FAILED",
            "error": str(e)
        }

    # ================= SAVE RESULTS =================
    os.makedirs("results", exist_ok=True)

    with open(RESULT_PATH, "w") as f:
        json.dump(result_data, f, indent=4)

    return result_data
