import os
from tools.live_logger import push_log


# ================= AUTO FIX ENGINE =================

def apply_ast_fixes(repo_path, issues):

    push_log("[AST AutoFix] Applying structural fixes...")

    fixes_applied = []

    # group issues by file
    files_map = {}

    for issue in issues:
        f = issue["file"]
        files_map.setdefault(f, []).append(issue)

    # process each file
    for file_path, file_issues in files_map.items():

        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            modified = False

            for issue in file_issues:

                line_no = issue.get("line", 0)

                if line_no <= 0 or line_no > len(lines):
                    continue

                idx = line_no - 1

                # 🔥 EMPTY FUNCTION FIX
                if issue["type"] == "EmptyFunction":
                    push_log(f"[AST AutoFix] Fixing empty function → {file_path}:{line_no}")

                    # add pass if missing
                    lines.insert(idx + 1, "    pass\n")
                    modified = True

                # 🔥 WILDCARD IMPORT FIX
                if issue["type"] == "WildcardImport":
                    push_log(f"[AST AutoFix] Removing wildcard import → {file_path}:{line_no}")

                    lines[idx] = "# removed wildcard import by AST AutoFix\n"
                    modified = True

                # 🔥 BASIC SYNTAX FIX (safe fallback)
                if issue["type"] == "SyntaxError":
                    push_log(f"[AST AutoFix] Commenting syntax error line → {file_path}:{line_no}")

                    lines[idx] = "# syntax error auto-commented by AST AutoFix\n"
                    modified = True

            if modified:

                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                fixes_applied.append({
                    "file": file_path,
                    "commit": "[AST-AUTO-FIX]"
                })

        except Exception as e:
            push_log(f"[AST AutoFix] Failed on {file_path}: {str(e)}")

    push_log(f"[AST AutoFix] Total fixes applied: {len(fixes_applied)}")

    return fixes_applied
