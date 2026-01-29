
from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
from tools import tools_runner
import re, os
from datetime import datetime

app = FastAPI()

# Configuration (mock for now, should be loaded securely)
API_KEY = "SuperSecretKey123"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input schema
class ToolRequest(BaseModel):
    tool: str
    target: str

# Basic target validation
def is_valid_target(target):
    domain_regex = re.compile(
        r"^(?!-)[A-Za-z0-9.-]{1,253}(?<!-)$"
    )
    ip_regex = re.compile(
        r"^(\d{1,3}\.){3}\d{1,3}$"
    )
    return domain_regex.match(target) or ip_regex.match(target)

@app.post("/run_tool")
async def run_tool(req: ToolRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not is_valid_target(req.target):
        raise HTTPException(status_code=400, detail="Invalid target format")

    result = tools_runner.run_tool(req.tool, req.target)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{req.tool}_{req.target.replace('.', '_')}_{timestamp}.log"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write("=== STDOUT ===\n")
        f.write(result.get("stdout", "") + "\n")
        f.write("=== STDERR ===\n")
        f.write(result.get("stderr", "") + "\n")

    response = {
        "status": "success" if result.get("returncode") == 0 else "error",
        "command": result.get("command"),
        "output_preview": result.get("stdout", "")[:1000],  # Preview first 1000 chars
        "log_file": filepath
    }
    return response
