import sys
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

# ⭐ telemetry DB import
from tools.telemetry_db import init_db


app = FastAPI(title="ALPHA DevOps Agent")

# ================= ROUTES =================
app.include_router(router)

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # dev mode
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= STARTUP EVENT =================
@app.on_event("startup")
def startup_event():
    init_db()   # ⭐ DB auto create


# ================= HEALTH CHECK =================
@app.get("/")
def home():
    return {"status": "Backend Running"}
