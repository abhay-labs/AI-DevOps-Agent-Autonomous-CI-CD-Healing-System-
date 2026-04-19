from tools.code_modifier import apply_fix
from tools.live_logger import push_log


def build_fix_message(bug_type, file, line):

    fixes = {
        "LINTING": "remove the unused import statement",
        "SYNTAX": "add the missing colon",
        "TYPE_ERROR": "correct variable type",
        "IMPORT": "fix incorrect import path",
        "INDENTATION": "fix indentation spacing",
        "LOGIC": "adjust logical condition"
    }

    fix = fixes.get(bug_type, "general code correction")

    return f"{bug_type} error in {file} line {line} → Fix: {fix}"


def generate_fixes(failures, repo_path):

    push_log("[Fix Agent] Applying AI fixes...")   # 👈 YAHAN

    fixes = []

    for f in failures:

        bug_type = f.get("type", "LOGIC")
        file = f.get("file")
        line = f.get("line")

        # 🔥 REAL FILE MODIFICATION
        apply_fix(repo_path, file, line, bug_type)

        msg = build_fix_message(bug_type, file, line)

        fixes.append({
            "file": file,
            "line": line,
            "bug_type": bug_type,
            "commit": f"[AI-AGENT] {msg}"
        })

    return fixes
