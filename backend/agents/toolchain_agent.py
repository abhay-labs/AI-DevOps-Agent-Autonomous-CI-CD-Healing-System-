import subprocess
from tools.live_logger import push_log


def run_cmd(cmd, cwd):

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            push_log(f"[Toolchain] Command failed: {cmd}")
            push_log(result.stderr)
        else:
            push_log(f"[Toolchain] Success: {cmd}")

    except Exception as e:
        push_log(f"[Toolchain] Error running {cmd}: {str(e)}")


def run_toolchain(repo_path, languages):

    push_log("[Toolchain Agent] Executing auto toolchain...")

    # 🐍 PYTHON
    if languages.get("python"):
        push_log("[Toolchain Agent] Python detected")

        run_cmd("pip install -r requirements.txt", repo_path)
        run_cmd("pytest --collect-only", repo_path)

    # 🟩 NODE
    if languages.get("node"):
        push_log("[Toolchain Agent] NodeJS detected")

        run_cmd("npm install", repo_path)
        run_cmd("npm run lint", repo_path)

    # 🐳 DOCKER
    if languages.get("docker"):
        push_log("[Toolchain Agent] Dockerfile detected")

        run_cmd("docker build -t ai-agent-test .", repo_path)

    push_log("[Toolchain Agent] Toolchain execution complete")
