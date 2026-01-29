from __future__ import annotations

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "Projects"
PROJECTS.mkdir(parents=True, exist_ok=True)

def _proj_dir(project_id: str) -> Path:
    safe = "".join(c for c in project_id if c.isalnum() or c in ("-","_","."))[:80]
    if not safe:
        raise ValueError("invalid project_id")
    return PROJECTS / safe

def create_project(project_id: str, owner: str, scope: dict) -> dict:
    pdir = _proj_dir(project_id)
    pdir.mkdir(parents=True, exist_ok=True)
    meta = {
        "project_id": project_id,
        "owner": owner,
        "created_at": int(time.time()),
        "status": "CREATED",
        "scope": scope,
        "history": [{"t": int(time.time()), "status": "CREATED"}]
    }
    (pdir/"meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (pdir/"logs").mkdir(exist_ok=True)
    return meta

def load_meta(project_id: str) -> dict:
    p = _proj_dir(project_id)/"meta.json"
    return json.loads(p.read_text(encoding="utf-8"))

def update_status(project_id: str, status: str, note: str="") -> dict:
    meta = load_meta(project_id)
    meta["status"] = status
    meta.setdefault("history", []).append({"t": int(time.time()), "status": status, "note": note})
    (_proj_dir(project_id)/"meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta

def list_projects() -> list[dict]:
    out = []
    for d in PROJECTS.iterdir():
        if d.is_dir() and (d/"meta.json").exists():
            out.append(json.loads((d/"meta.json").read_text(encoding="utf-8")))
    return sorted(out, key=lambda x: x.get("created_at", 0), reverse=True)
