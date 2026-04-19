import os
import uuid
import subprocess
from tools.live_logger import push_log

BASE_WORKSPACE = "workspaces"


# ================= RUN COMMAND =================

def run_cmd(cmd, cwd=None):

    process = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=True
    )

    if process.returncode != 0:
        push_log(process.stderr)

    return process


# ================= CLONE REPO =================

def clone_repo(repo_url):

    if not repo_url:
        raise Exception("Repository URL empty")

    os.makedirs(BASE_WORKSPACE, exist_ok=True)

    unique_id = str(uuid.uuid4())[:8]
    folder = os.path.join(BASE_WORKSPACE, f"repo_{unique_id}")

    push_log(f"[Repo Agent] Creating workspace: {folder}")

    try:

        # ⭐ FULL SHALLOW CLONE (FAST + RELIABLE)
        cmd = f"git clone --depth 1 {repo_url} {folder}"

        result = run_cmd(cmd)

        if result.returncode != 0:
            raise Exception("Git clone failed")

        push_log("[Repo Agent] Shallow clone completed")

        # ⭐ FIX: अगर repo extra root folder में हो
        inner_items = os.listdir(folder)

        if len(inner_items) == 1:
            inner_path = os.path.join(folder, inner_items[0])

            if os.path.isdir(inner_path):
                push_log("[Repo Agent] Detected nested repo structure → flattening")

                for item in os.listdir(inner_path):
                    os.rename(
                        os.path.join(inner_path, item),
                        os.path.join(folder, item)
                    )

                os.rmdir(inner_path)

        push_log("[Repo Agent] Repository cloned successfully")

        return folder

    except Exception as e:

        push_log(f"[Repo Agent] Clone Failed: {str(e)}")
        raise Exception("Repository clone failed")
