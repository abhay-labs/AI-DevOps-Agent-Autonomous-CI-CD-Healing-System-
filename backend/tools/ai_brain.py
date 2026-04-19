from tools.live_logger import push_log


def ai_think(message):

    push_log(f"🤖 AI: {message}")


def decide_strategy(languages):

    ai_think("Analyzing repository structure...")

    if languages.get("multi"):
        ai_think("Multi-language project detected. Using hybrid strategy.")
        return "HYBRID"

    if languages.get("python"):
        ai_think("Python stack detected. Choosing pytest strategy.")
        return "PYTHON"

    if languages.get("node"):
        ai_think("NodeJS stack detected. Choosing npm strategy.")
        return "NODE"

    ai_think("Unknown stack. Running universal scan.")
    return "GENERIC"
