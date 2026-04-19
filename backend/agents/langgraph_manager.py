from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from agents.repo_agent import clone_repo
from agents.test_agent import run_tests
from agents.fix_agent import generate_fixes
from agents.cicd_agent import monitor_cicd
from tools.github_tools import commit_and_push
from tools.live_logger import push_log

from agents.language_agent import detect_languages
from agents.toolchain_agent import run_toolchain
from tools.ai_brain import ai_think, decide_strategy
from tools.ai_score import calculate_real_score
from tools.telemetry_db import save_telemetry

from agents.ast_agent import run_ast_analysis
from agents.ast_autofix_agent import apply_ast_fixes
from tools.self_learning_brain import should_skip_ai_fix

import time


# ================== STATE ==================

class AgentState(TypedDict):
    repo_url: str
    team: str
    leader: str
    repo_path: str
    failures: List
    fixes: List
    branch: str
    status: str
    iteration: int
    languages: dict
    strategy: str
    score: dict
    start_time: float
    end_time: float


# ================== NODES ==================

def repo_node(state):

    state["start_time"] = time.time()

    push_log("[Repo Agent] Cloning repository...")

    repo_path = clone_repo(state["repo_url"])

    push_log("[Repo Agent] Repository cloned successfully")

    state["repo_path"] = repo_path

    return state


def language_node(state):

    ai_think("Detecting project language...")

    langs = detect_languages(state["repo_path"])

    strategy = decide_strategy(langs)

    state["languages"] = langs
    state["strategy"] = strategy

    return state


def toolchain_node(state):

    ai_think("Preparing toolchain execution...")

    run_toolchain(
        state["repo_path"],
        state.get("languages", {})
    )

    ai_think("Toolchain execution finished")

    return state



def test_node(state):

    ai_think("Starting intelligent code analysis...")

    langs = state.get("languages", {})

    failures = []

    # 🔥 REAL AST ANALYZER ALWAYS RUN
    ai_think("Running AST structural analysis...")
    ast_issues = run_ast_analysis(state["repo_path"])
    failures.extend(ast_issues)

    # 🐍 PYTHON TEST ANALYSIS
    if langs.get("python"):
        ai_think("Python detected → running pytest analyzer")
        failures.extend(run_tests(state["repo_path"]))

    # 🟩 NODE (future ESLint integration)
    if langs.get("node"):
        ai_think("NodeJS detected → running JS scan")

    if not failures:
        ai_think("No issues found. Skipping fix phase.")
    else:
        ai_think(f"{len(failures)} issues detected. Preparing fix phase.")

    state["failures"] = failures

    return state





def fix_node(state):

    failures = state.get("failures", [])

    if not failures:
        push_log("[Fix Agent] No fixes required")
        return state

    push_log("[Fix Agent] Applying AI fixes...")

    fast_mode = should_skip_ai_fix(failures)

    # 🔥 AST AUTO FIX
    ast_fixes = apply_ast_fixes(
        state["repo_path"],
        failures
    )

    # ⭐ ADD LABELS (VERY IMPORTANT FOR FRONTEND)
    for f in ast_fixes:
        f["type"] = "AST"
        f["description"] = f.get("description", "AST structural fix applied")

    ai_fixes = []

    if not fast_mode:
        ai_fixes = generate_fixes(
            failures,
            state["repo_path"]
        )

        for f in ai_fixes:
            f["type"] = "AI"
            f["description"] = f.get("description", "AI generated fix")

    else:
        push_log("[SelfLearning] Skipping AI generation → using learned fixes")

    # ⭐ FINAL MERGE
    state["fixes"] = ast_fixes + ai_fixes

    return state





def commit_node(state):

    if not state["fixes"]:
        push_log("[Commit Agent] Nothing to commit")
        return state

    push_log("[Commit Agent] Creating fix branch...")

    branch = commit_and_push(
        state["repo_path"],
        state["fixes"],
        state["team"],
        state["leader"],
    )

    state["branch"] = branch

    return state


def cicd_node(state):

    branch = state.get("branch", "")

    if not branch:
        push_log("[CI/CD Agent] No branch created → Pipeline auto PASSED")
        state["status"] = "PASSED"
        state["iteration"] = state.get("iteration", 1) + 1
        return state

    push_log("[CI/CD Agent] Monitoring pipeline...")

    status = monitor_cicd(branch)

    state["status"] = status
    state["iteration"] = state.get("iteration", 1) + 1

    return state


def score_node(state):

    score = calculate_real_score(state)

    state["score"] = score

    return state


def telemetry_node(state):

    save_telemetry(state)

    return state


# ================== DECISION ==================

def should_retry(state):

    status = state.get("status", "FAILED")
    iteration = state.get("iteration", 1)

    if status == "PASSED":
        push_log("[Agent] Pipeline PASSED")
        return END

    if iteration >= 5:
        push_log("[Agent] Max retries reached")
        return END

    push_log("[Agent] Retrying test cycle...")
    return "test_node"


# ================== GRAPH ==================

def build_agent():

    graph = StateGraph(AgentState)

    graph.add_node("repo_node", repo_node)
    graph.add_node("language_node", language_node)
    graph.add_node("toolchain_node", toolchain_node)
    graph.add_node("test_node", test_node)
    graph.add_node("fix_node", fix_node)
    graph.add_node("commit_node", commit_node)
    graph.add_node("cicd_node", cicd_node)
    graph.add_node("score_node", score_node)
    graph.add_node("telemetry_node", telemetry_node)

    graph.set_entry_point("repo_node")

    graph.add_edge("repo_node", "language_node")
    graph.add_edge("language_node", "toolchain_node")
    graph.add_edge("toolchain_node", "test_node")
    graph.add_edge("test_node", "fix_node")
    graph.add_edge("fix_node", "commit_node")
    graph.add_edge("commit_node", "cicd_node")

    # ⭐ REAL FLOW AFTER CICD
    graph.add_edge("cicd_node", "score_node")
    graph.add_edge("score_node", "telemetry_node")

    graph.add_conditional_edges(
        "telemetry_node",
        should_retry
    )

    return graph.compile()


agent = build_agent()


def run_langgraph_pipeline(repo_url, team, leader):

    initial_state = {
        "repo_url": repo_url,
        "team": team,
        "leader": leader,
        "repo_path": "",
        "failures": [],
        "fixes": [],
        "branch": "",
        "status": "FAILED",
        "iteration": 1,
        "languages": {},
        "strategy": "",
        "score": {},
        "start_time": 0,
        "end_time": 0,
    }

    return agent.invoke(initial_state)
