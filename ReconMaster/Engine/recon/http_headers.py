from __future__ import annotations

import requests
from .._base import Module, ModuleResult

class HTTPHeaders(Module):
    id = "recon.http_headers"
    title = "HTTP Header Baseline"

    def run(self, target: dict, context: dict) -> ModuleResult:
        url = target.get("url", "")
        findings = []
        meta = {}
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "ReconMaster-Client/1.0"}, allow_redirects=True)
            meta["status_code"] = r.status_code
            headers = {k.lower(): v for k, v in r.headers.items()}
            recommended = [
                "content-security-policy",
                "strict-transport-security",
                "x-content-type-options",
                "x-frame-options",
                "referrer-policy",
                "permissions-policy",
            ]
            missing = [h for h in recommended if h not in headers]
            if missing:
                findings.append({
                    "severity": "info",
                    "type": "missing_headers",
                    "message": "Empfohlene Security-Header fehlen",
                    "details": {"missing": missing}
                })
            return ModuleResult(ok=True, title=self.title, findings=findings, meta=meta)
        except Exception as e:
            return ModuleResult(ok=False, title=self.title, findings=[{"severity":"error","message":str(e)}], meta=meta)
