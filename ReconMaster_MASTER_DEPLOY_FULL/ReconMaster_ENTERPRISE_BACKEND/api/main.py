# FastAPI starter for tool control + logging
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "ReconMaster Enterprise API running"}

@app.post("/run-tool")
def run_tool(request: Request):
    return {"status": "Tool triggered"}

@app.post("/log-action")
def log_action(action: str, user: str, tool: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "action": action,
        "tool": tool
    }
    with open("../logs/actions.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    return {"status": "logged"}
