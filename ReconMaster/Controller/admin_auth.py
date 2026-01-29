from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
import bcrypt
import sys
import requests

ROOT = Path(__file__).resolve().parent
CFG_PATHS = [
    ROOT.parent / "Admin" / "admin.conf",
    ROOT / "admin.conf",
]

def _load_admin_cfg() -> ConfigParser:
    cfg = ConfigParser()
    for p in CFG_PATHS:
        if p.exists():
            cfg.read(str(p))
            return cfg
    raise FileNotFoundError("admin.conf not found")

_cfg = _load_admin_cfg()

ADMIN_USER = _cfg.get("DEFAULT", "admin_user", fallback="admin")
ADMIN_HASH = _cfg.get("DEFAULT", "admin_pass_hash").encode()
FORMSPREE = _cfg.get("DEFAULT", "formspree_endpoint", fallback="")

def admin_login() -> None:
    username = input("Admin Username: ").strip()
    password = input("Admin Passwort: ")

    if username != ADMIN_USER:
        print("Zugriff verweigert")
        sys.exit(1)

    if not bcrypt.checkpw(password.encode(), ADMIN_HASH):
        print("Zugriff verweigert")
        sys.exit(1)

    if FORMSPREE:
        try:
            requests.post(FORMSPREE, data={"message": f"Admin login: {username}"}, timeout=5)
        except Exception:
            pass
