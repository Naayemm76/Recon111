
from fastapi import FastAPI, Request, Form, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tools import tools_runner
from tools.tools_registry import TOOL_REGISTRY
import re, os
from datetime import datetime

app = FastAPI()

API_KEY = "SuperSecretKey123"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

templates = Jinja2Templates(directory="templates")

def is_valid_target(target):
    domain_regex = re.compile(r"^(?!-)[A-Za-z0-9.-]{1,253}(?<!-)$")
    ip_regex = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
    return domain_regex.match(target) or ip_regex.match(target)

@app.get("/", response_class=HTMLResponse)
async def ui_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tools": TOOL_REGISTRY})

@app.post("/run_tool_ui", response_class=HTMLResponse)
async def run_tool_ui(request: Request, tool: str = Form(...), target: str = Form(...)):
    if not is_valid_target(target):
        raise HTTPException(status_code=400, detail="Invalid target format")

    result = tools_runner.run_tool(tool, target)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{tool}_{target.replace('.', '_')}_{timestamp}.log"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w") as f:
        f.write("=== STDOUT ===\n")
        f.write(result.get("stdout", "") + "\n")
        f.write("=== STDERR ===\n")
        f.write(result.get("stderr", "") + "\n")

    response = {
        "status": "success" if result.get("returncode") == 0 else "error",
        "command": result.get("command"),
        "output_preview": result.get("stdout", "")[:2000],
        "log_file": filepath
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "tools": TOOL_REGISTRY,
        "result": response
    })

@app.post("/run_tool")
async def run_tool_api(tool: str = Form(...), target: str = Form(...), x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not is_valid_target(target):
        raise HTTPException(status_code=400, detail="Invalid target format")

    result = tools_runner.run_tool(tool, target)
    return result

@app.get("/list_tools")
async def list_tools():
    return TOOL_REGISTRY
