import os
import ast
from tools.live_logger import push_log


# ================= REAL AST SCANNER =================

def run_ast_analysis(repo_path):

    push_log("[AST Analyzer] Running deep AST scan...")

    issues = []

    total_files = 0

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if not file.lower().endswith(".py"):
                continue

            total_files += 1

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()

                # 🔥 TRY PARSE
                tree = ast.parse(code)

                # ⭐ Walk AST Nodes
                for node in ast.walk(tree):

                    # Broken function (empty body)
                    if isinstance(node, ast.FunctionDef):
                        if not node.body:
                            issues.append({
                                "file": file_path,
                                "line": node.lineno,
                                "type": "EmptyFunction",
                                "msg": "Function has no body"
                            })

                    # Unsafe import check
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name == "*":
                                issues.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "type": "WildcardImport",
                                    "msg": "Wildcard import detected"
                                })

            except SyntaxError as e:

                issues.append({
                    "file": file_path,
                    "line": e.lineno,
                    "type": "SyntaxError",
                    "msg": str(e)
                })

            except IndentationError as e:

                issues.append({
                    "file": file_path,
                    "line": e.lineno,
                    "type": "IndentationError",
                    "msg": str(e)
                })

            except Exception:
                pass

    push_log(f"[AST Analyzer] Files scanned: {total_files}")
    push_log(f"[AST Analyzer] Issues found: {len(issues)}")

    return issues
