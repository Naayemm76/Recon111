from __future__ import annotations

from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str="reconmaster"):
    log = logging.getLogger(name)
    if log.handlers:
        return log
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_DIR/"controller.log", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh.setFormatter(fmt)
    log.addHandler(fh)
    return log
