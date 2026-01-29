import json
import os
from datetime import datetime

DEFAULT_META = {
    "status": "CREATED",
    "legal": {
        "analysis": False,
        "exploit": False
    },
    "role": "viewer",
    "history": []
}

def meta_path(project):
    return os.path.join("Projects", project, "meta.json")

def load_meta(project):
    path = meta_path(project)
    if not os.path.exists(path):
        return DEFAULT_META.copy()
    with open(path, "r") as f:
        return json.load(f)

def save_meta(project, meta):
    path = meta_path(project)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(meta, f, indent=2)

def update_status(project, status):
    meta = load_meta(project)
    meta["status"] = status
    meta["history"].append({
        "time": datetime.utcnow().isoformat(),
        "status": status
    })
    save_meta(project, meta)

def allow_exploit(project):
    meta = load_meta(project)
    return (
        meta["status"] == "EXPLOIT_ALLOWED"
        and meta["legal"]["exploit"] is True
    )
