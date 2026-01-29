from __future__ import annotations

from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "Projects"
PROJECTS.mkdir(parents=True, exist_ok=True)

def ensure_project(project_id: str) -> Path:
    p = PROJECTS / project_id
    p.mkdir(parents=True, exist_ok=True)
    (p / "imports").mkdir(parents=True, exist_ok=True)
    return p

def _meta_path(project_id: str) -> Path:
    return ensure_project(project_id) / "meta.json"

def load_meta(project_id: str) -> dict:
    mp = _meta_path(project_id)
    if mp.exists():
        return json.loads(mp.read_text(encoding="utf-8"))
    meta = {"id": project_id, "status": "NEW", "created_at": int(time.time())}
    mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return meta

def save_meta(project_id: str, meta: dict) -> None:
    mp = _meta_path(project_id)
    mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

def update_status(project_id: str, status: str, stage: str = "") -> None:
    meta = load_meta(project_id)
    meta["status"] = status
    meta["stage"] = stage
    meta["updated_at"] = int(time.time())
    save_meta(project_id, meta)
