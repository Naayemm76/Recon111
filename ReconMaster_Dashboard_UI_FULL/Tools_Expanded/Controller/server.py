from __future__ import annotations

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import secrets
import time
import json

from .logger import get_logger
from . import admin_auth
from . import legal_gate
from . import project_meta
from . import workflow

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
TEMPLATES = Jinja2Templates(directory=str(UI / "templates"))
log = get_logger()

app = FastAPI(title="ReconMaster UI")
app.mount("/static", StaticFiles(directory=str(UI)), name="static")

SESSIONS = {}

def _session_user(request: Request) -> str | None:
    sid = request.cookies.get("rm_sid")
    if not sid:
        return None
    return SESSIONS.get(sid)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return TEMPLATES.TemplateResponse("login.html", {"request": request, "error": ""})

@app.post("/login", response_class=HTMLResponse)
def do_login(request: Request,
             username: str = Form(...),
             password: str = Form(...),
             accept_terms: str = Form(None)):
    if not accept_terms:
        return TEMPLATES.TemplateResponse("login.html", {"request": request, "error": "Bitte Bedingungen akzeptieren."})
    ok = admin_auth.verify(username, password)
    if not ok:
        return TEMPLATES.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    sid = secrets.token_urlsafe(24)
    SESSIONS[sid] = username
    resp = TEMPLATES.TemplateResponse("dashboard.html", {"request": request, "user": username, "projects": project_meta.list_projects()})
    resp.set_cookie("rm_sid", sid, httponly=True, samesite="lax")
    return resp

@app.get("/terms", response_class=PlainTextResponse)
def terms():
    p = ROOT.parent / "Legal" / "TERMS.txt"
    return p.read_text(encoding="utf-8") if p.exists() else ""

@app.post("/projects/create", response_class=JSONResponse)
def create_project(request: Request,
                   project_id: str = Form(...),
                   url: str = Form(...)):
    user = _session_user(request)
    if not user:
        return JSONResponse({"ok": False, "error": "not_authenticated"}, status_code=401)
    meta = project_meta.create_project(project_id, user, {"url": url})
    return JSONResponse({"ok": True, "project": meta})

@app.post("/projects/run", response_class=JSONResponse)
def run_project(request: Request,
                project_id: str = Form(...)):
    user = _session_user(request)
    if not user:
        return JSONResponse({"ok": False, "error": "not_authenticated"}, status_code=401)
    if not legal_gate.has_accepted(user, project_id):
        legal_gate.accept(user, project_id)
    meta = project_meta.load_meta(project_id)
    report = workflow.run_pipeline(project_id, {"url": meta["scope"]["url"]})
    return JSONResponse({"ok": True, "report": report})

@app.get("/projects/list", response_class=JSONResponse)
def list_projects(request: Request):
    user = _session_user(request)
    if not user:
        return JSONResponse({"ok": False, "error": "not_authenticated"}, status_code=401)
    return JSONResponse({"ok": True, "projects": project_meta.list_projects()})
