from __future__ import annotations

from pathlib import Path
import sqlite3
import time
import hashlib

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "Legal" / "accepted.sqlite3"
ROOT.joinpath("Legal").mkdir(exist_ok=True)

def _db():
    con = sqlite3.connect(str(DB))
    con.execute(
        "CREATE TABLE IF NOT EXISTS accepted ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user TEXT NOT NULL,"
        "project_id TEXT NOT NULL,"
        "terms_sha256 TEXT NOT NULL,"
        "accepted_at INTEGER NOT NULL"
        ")"
    )
    return con

def terms_hash() -> str:
    terms = (ROOT/"Legal"/"TERMS.txt").read_bytes() if (ROOT/"Legal"/"TERMS.txt").exists() else b""
    return hashlib.sha256(terms).hexdigest()

def has_accepted(user: str, project_id: str) -> bool:
    con = _db()
    h = terms_hash()
    cur = con.execute("SELECT 1 FROM accepted WHERE user=? AND project_id=? AND terms_sha256=? LIMIT 1", (user, project_id, h))
    row = cur.fetchone()
    con.close()
    return bool(row)

def accept(user: str, project_id: str) -> None:
    con = _db()
    h = terms_hash()
    con.execute("INSERT INTO accepted(user, project_id, terms_sha256, accepted_at) VALUES(?,?,?,?)",
                (user, project_id, h, int(time.time())))
    con.commit()
    con.close()
