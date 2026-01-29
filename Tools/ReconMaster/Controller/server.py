from __future__ import annotations

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import time
import secrets
import hashlib
import os

from .project_meta import ensure_project, load_meta, save_meta
from .workflow import process_import

ROOT = Path(__file__).resolve().parent
UI = ROOT / "ui"
LEGAL = ROOT.parent / "Legal"
LOGS = ROOT / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory=str(UI / "templates"))

app.mount("/static", StaticFiles(directory=str(UI)), name="static")

def _safe_id(prefix: str = "p") -> str:
    return prefix + secrets.token_hex(6)

def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()

def load_cfg() -> dict:
    p = ROOT / "config.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    p2 = ROOT.parent / "config.json"
    if p2.exists():
        return json.loads(p2.read_text(encoding="utf-8"))
    return {}

CFG = load_cfg()

@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "langs": CFG.get("languages", ["DE","EN"]), "default_lang": CFG.get("default_lang","DE")})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/legal/{doc}", response_class=PlainTextResponse)
def legal_doc(doc: str):
    allowed = {"TERMS.txt", "DISCLAIMER.txt", "LEGAL_NOTICE.txt"}
    if doc not in allowed:
        return PlainTextResponse("Not found", status_code=404)
    p = LEGAL / doc
    return PlainTextResponse(p.read_text(encoding="utf-8"), status_code=200)

@app.post("/api/projects/create", response_class=JSONResponse)
def api_create_project(name: str = Form(...), target_type: str = Form(...), target_value: str = Form(...)):
    project_id = _safe_id("proj_")
    base = ensure_project(project_id)
    meta = {
        "id": project_id,
        "name": name,
        "target": {"type": target_type, "value": target_value},
        "status": "CREATED",
        "created_at": int(time.time()),
        "imports": [],
        "findings": {"critical":0,"high":0,"medium":0,"low":0,"info":0},
    }
    save_meta(project_id, meta)
    return {"ok": True, "project_id": project_id, "meta": meta}

@app.post("/api/projects/{project_id}/import", response_class=JSONResponse)
def api_import(project_id: str, importer: str = Form(...), f: UploadFile = File(...)):
    base = ensure_project(project_id)
    imp_dir = base / "imports"
    imp_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    safe_name = f"{ts}_{secrets.token_hex(4)}_{Path(f.filename).name}"
    dest = imp_dir / safe_name
    with dest.open("wb") as out:
        out.write(f.file.read())

    res = process_import(project_id, dest, importer)

    meta = load_meta(project_id)
    meta.setdefault("imports", []).append({"file": safe_name, "importer": importer, "ts": ts, "count": res.get("count",0)})
    save_meta(project_id, meta)

    return res | {"file": safe_name}

@app.get("/api/projects/{project_id}/meta", response_class=JSONResponse)
def api_meta(project_id: str):
    return {"ok": True, "meta": load_meta(project_id)}

@app.get("/api/projects/list", response_class=JSONResponse)
def api_list():
    projects_root = ROOT.parent / "Projects"
    projects_root.mkdir(parents=True, exist_ok=True)
    out = []
    for p in projects_root.iterdir():
        if not p.is_dir():
            continue
        mp = p / "meta.json"
        if mp.exists():
            try:
                out.append(json.loads(mp.read_text(encoding="utf-8")))
            except Exception:
                continue
    out.sort(key=lambda x: x.get("created_at",0), reverse=True)
    return {"ok": True, "projects": out}
