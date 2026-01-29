
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from tools import tools_runner
import re

app = FastAPI()

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
async def run_tool(req: ToolRequest):
    if not is_valid_target(req.target):
        raise HTTPException(status_code=400, detail="Invalid target format")

    result = tools_runner.run_tool(req.tool, req.target)
    return result
