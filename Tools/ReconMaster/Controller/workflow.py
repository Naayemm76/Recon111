from __future__ import annotations

from pathlib import Path
import json
import time
from dataclasses import asdict

from .logger import get_logger
from .project_meta import update_status

ROOT = Path(__file__).resolve().parent.parent
log = get_logger()

def process_import(project_id: str, import_file: Path, importer: str) -> dict:
    update_status(project_id, "RUNNING", "import_processing")
    findings = []
    if importer == "nmap_xml":
        from Engine.modules.importers.nmap_xml import parse_nmap_xml
        findings = [asdict(f) for f in parse_nmap_xml(import_file)]
    elif importer == "lines":
        from Engine.modules.importers.lines import parse_lines
        findings = [asdict(f) for f in parse_lines(import_file)]
    else:
        update_status(project_id, "FAILED", "unknown_importer")
        return {"ok": False, "error": "unknown_importer"}

    update_status(project_id, "DONE", "import_done")
    return {"ok": True, "findings": findings, "count": len(findings), "importer": importer, "ts": int(time.time())}
