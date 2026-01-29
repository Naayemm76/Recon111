from __future__ import annotations

from pathlib import Path
import importlib
import json
import time

from .logger import get_logger
from .project_meta import update_status

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "Engine"
MODULES_DIR = ENGINE / "modules"
log = get_logger()

DEFAULT_PIPELINE = [
    "Engine.modules.recon.http_headers:HTTPHeaders",
    "Engine.modules.analysis.robots_txt:RobotsTxt",
]

def run_pipeline(project_id: str, target: dict, pipeline: list[str] | None = None) -> dict:
    pipeline = pipeline or DEFAULT_PIPELINE
    update_status(project_id, "RUNNING", "pipeline_start")
    all_findings=[]
    results=[]
    ctx={"project_id": project_id, "started_at": int(time.time())}

    for spec in pipeline:
        mod_path, cls_name = spec.split(":")
        log.info(f"RUN {spec} target={target}")
        try:
            mod = importlib.import_module(mod_path)
            cls = getattr(mod, cls_name)
            inst = cls()
            res = inst.run(target, ctx)
            payload = {"id": getattr(inst, "id", spec), "title": res.title, "ok": res.ok, "findings": res.findings, "meta": res.meta}
            results.append(payload)
            all_findings.extend(res.findings)
        except Exception as e:
            results.append({"id": spec, "title": spec, "ok": False, "findings":[{"severity":"error","message":str(e)}], "meta":{}})

    report = {"project_id": project_id, "target": target, "results": results, "findings": all_findings}
    out = ROOT/"Projects"/project_id/"report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    update_status(project_id, "DONE", "pipeline_done")
    return report
