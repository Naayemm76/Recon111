from __future__ import annotations

import requests
from .._base import Module, ModuleResult

class RobotsTxt(Module):
    id = "analysis.robots_txt"
    title = "robots.txt Discovery"

    def run(self, target: dict, context: dict) -> ModuleResult:
        base = target.get("url","").rstrip("/")
        url = base + "/robots.txt"
        findings=[]
        meta={}
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent":"ReconMaster-Client/1.0"})
            meta["status_code"]=r.status_code
            if r.status_code == 200 and "Disallow" in r.text:
                dis = [line.strip() for line in r.text.splitlines() if line.strip().lower().startswith("disallow")]
                findings.append({"severity":"info","type":"robots_disallow","message":"robots.txt enthält Disallow-Einträge","details":{"lines":dis}})
            return ModuleResult(ok=True, title=self.title, findings=findings, meta=meta)
        except Exception as e:
            return ModuleResult(ok=False, title=self.title, findings=[{"severity":"error","message":str(e)}], meta=meta)
