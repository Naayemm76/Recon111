from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import time
import secrets
import hashlib
import os
import requests

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
LEGAL = ROOT.parent / "Legal"
LOGS = ROOT / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

def load_cfg():
    p = ROOT / "config.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    p2 = ROOT.parent / "config.json"
    if p2.exists():
        return json.loads(p2.read_text(encoding="utf-8"))
    return {}

CFG = load_cfg()

SESS = {}
COOKIE = "rm_session"

def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def now():
    return int(time.time())

def write_log(line):
    (LOGS / "controller.log").open("a", encoding="utf-8").write(line + "\n")

def user_from_req(req: Request):
    sid = req.cookies.get(COOKIE, "")
    if not sid or sid not in SESS:
        return None
    sess = SESS[sid]
    if sess.get("exp", 0) < now():
        del SESS[sid]
        return None
    return sess

def require_user(req: Request):
    u = user_from_req(req)
    if not u:
        raise Exception("unauthorized")
    return u

app = FastAPI()
app.mount("/ui", StaticFiles(directory=str(UI)), name="ui")

@app.get("/", response_class=HTMLResponse)
def page_login():
    return (UI / "templates" / "login.html").read_text(encoding="utf-8")

@app.get("/app", response_class=HTMLResponse)
def page_app(req: Request):
    u = user_from_req(req)
    if not u:
        return RedirectResponse("/", status_code=302)
    return (UI / "templates" / "app.html").read_text(encoding="utf-8")

@app.get("/api/legal/terms")
def get_terms():
    p = LEGAL / "TERMS.txt"
    if p.exists():
        return PlainTextResponse(p.read_text(encoding="utf-8"))
    return PlainTextResponse("TERMS.txt missing", status_code=404)

@app.post("/api/login")
async def api_login(req: Request):
    data = await req.json()
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "")
    accept = bool(data.get("accept"))
    if not accept:
        return PlainTextResponse("Terms not accepted", status_code=400)
    users = (CFG.get("users") or {})
    u = users.get(username)
    if not u:
        write_log(f"[{now()}] login_fail {username}")
        return PlainTextResponse("Invalid credentials", status_code=401)
    if sha256(password) != u.get("pass_sha256"):
        write_log(f"[{now()}] login_fail {username}")
        return PlainTextResponse("Invalid credentials", status_code=401)
    sid = secrets.token_urlsafe(32)
    SESS[sid] = {"username": username, "role": u.get("role","viewer"), "exp": now() + int(CFG.get("session_ttl_sec", 3600))}
    write_log(f"[{now()}] login_ok {username}")
    r = JSONResponse({"ok": True})
    r.set_cookie(COOKIE, sid, httponly=True, samesite="strict")
    return r

@app.post("/api/logout")
def api_logout(req: Request):
    sid = req.cookies.get(COOKIE, "")
    if sid in SESS:
        del SESS[sid]
    r = JSONResponse({"ok": True})
    r.delete_cookie(COOKIE)
    return r

@app.get("/api/me")
def api_me(req: Request):
    u = require_user(req)
    return {"username": u["username"], "role": u["role"]}

PROJECTS = {}

@app.post("/api/projects/create")
async def api_project_create(req: Request):
    u = require_user(req)
    data = await req.json()
    pid = secrets.token_hex(8)
    PROJECTS[pid] = {"id": pid, "name": data.get("name",""), "target": data.get("target",""), "scope": data.get("scope",""), "owner": u["username"]}
    pdir = ROOT.parent / "Projects" / pid
    (pdir / "logs").mkdir(parents=True, exist_ok=True)
    (pdir / "logs" / "run.log").open("a", encoding="utf-8").write(f"[{now()}] project_created {u['username']}\n")
    return {"ok": True, "id": pid}

@app.get("/api/projects")
def api_projects(req: Request):
    u = require_user(req)
    lst = list(PROJECTS.values())
    if u["role"] != "admin":
        lst = [p for p in lst if p.get("owner") == u["username"]]
    if not lst:
        pid = "demo"
        PROJECTS[pid] = {"id": pid, "name": "Demo", "target": "example.com", "scope": "demo", "owner": u["username"]}
        (ROOT.parent / "Projects" / pid / "logs").mkdir(parents=True, exist_ok=True)
        lst = [PROJECTS[pid]]
    return {"projects": lst}

@app.get("/api/logs/tail")
def api_logs_tail(req: Request, project: str):
    u = require_user(req)
    pdir = ROOT.parent / "Projects" / project / "logs" / "run.log"
    if not pdir.exists():
        return PlainTextResponse("", status_code=200)
    txt = pdir.read_text(encoding="utf-8", errors="ignore")
    lines = txt.splitlines()[-250:]
    return PlainTextResponse("\n".join(lines))

@app.get("/api/modules")
def api_modules(req: Request):
    u = require_user(req)
    role = u.get("role","viewer")
    items = [
        {"id":"intake", "title":"Project Intake", "explain":"Erfasst Scope, Zustimmung, Nachweise und Freigabe-Status.", "policy":"Always", "state":"Ready", "enabled": True, "action":"Open"},
        {"id":"surface", "title":"Surface Mapping", "explain":"Inventarisiert Assets und erzeugt eine nachvollziehbare Angriffsflächen-Zusammenfassung.", "policy":"Approval", "state":"Locked", "enabled": role in ("admin","lead","pentester"), "action":"Run"},
        {"id":"risk", "title":"Risk Correlation", "explain":"Konsolidiert Findings, bewertet Risiko und erklärt jeden Schritt.", "policy":"Approval", "state":"Locked", "enabled": role in ("admin","lead","pentester"), "action":"Run"},
        {"id":"report", "title":"Reporting", "explain":"Erstellt Audit-Trail, Management Summary und technische Anhänge.", "policy":"Always", "state":"Ready", "enabled": True, "action":"Run"}
    ]
    return items

@app.post("/api/modules/run")
async def api_modules_run(req: Request):
    u = require_user(req)
    data = await req.json()
    module_id = data.get("module_id","")
    project = data.get("project","")
    pdir = ROOT.parent / "Projects" / project / "logs"
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "run.log").open("a", encoding="utf-8").write(f"[{now()}] module_run {module_id} by {u['username']}\n")
    return {"ok": True}

@app.post("/api/support")
async def api_support(req: Request):
    data = await req.json()
    endpoint = (CFG.get("formspree") or {}).get("endpoint","")
    if not endpoint:
        return PlainTextResponse("Support endpoint missing", status_code=500)
    payload = {
        "email": data.get("email",""),
        "category": data.get("category",""),
        "message": data.get("message",""),
        "lang": data.get("lang","")
    }
    try:
        requests.post(endpoint, data=payload, timeout=10)
    except Exception:
        return PlainTextResponse("Send failed", status_code=502)
    return {"ok": True}
