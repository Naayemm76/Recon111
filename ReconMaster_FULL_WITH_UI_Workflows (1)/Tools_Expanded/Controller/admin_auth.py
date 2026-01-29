from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
import bcrypt

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "Admin" / "admin.conf"

def _cfg():
    c = ConfigParser()
    c.read(str(CFG))
    return c

def verify(username: str, password: str) -> bool:
    c = _cfg()
    if not c.has_section("DEFAULT") and not c.defaults():
        return False
    admin_user = c.get("DEFAULT", "admin_user", fallback="")
    admin_hash = c.get("DEFAULT", "admin_pass_hash", fallback="").encode()
    if username != admin_user or not admin_hash:
        return False
    return bcrypt.checkpw(password.encode(), admin_hash)

def make_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
