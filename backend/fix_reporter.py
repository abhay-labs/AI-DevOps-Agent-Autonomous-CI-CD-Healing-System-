from tools.live_logger import push_log


def build_fix_report(failures, fixes):

    report = []

    for issue in failures:

        file = issue.get("file", "unknown")
        line = issue.get("line", 0)
        err = issue.get("type", "UnknownError")

        fix_msg = "AI Generated Fix"

        # अगर AST autofix था
        for f in fixes:
            if f.get("file") == file:
                fix_msg = f.get("commit", "AutoFix Applied")

        report.append({
            "file": file,
            "line": line,
            "error": err,
            "fix": fix_msg
        })

    push_log(f"[FixReporter] Total fixes explained: {len(report)}")

    return report
