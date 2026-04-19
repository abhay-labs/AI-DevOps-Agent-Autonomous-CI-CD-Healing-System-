from fastapi import APIRouter
from agents.langgraph_manager import run_langgraph_pipeline

from fastapi.responses import StreamingResponse
from tools.live_logger import stream_logs


router = APIRouter()

@router.post("/run-agent")
def run_agent(data: dict):
    repo_url = data.get("repo_url")
    team = data.get("team")
    leader = data.get("leader")

    result = run_langgraph_pipeline(repo_url, team, leader)

    return result




@router.get("/stream-logs")
def get_logs():
    return StreamingResponse(stream_logs(), media_type="text/event-stream")
