from __future__ import annotations

def score(findings: list[dict]) -> dict:
    weight = {"critical": 100, "high": 60, "medium": 35, "low": 15, "info": 5, "error": 0}
    total = 0
    for f in findings:
        total += weight.get(str(f.get("severity","info")).lower(), 0)
    if total > 100:
        total = 100
    return {"score": total}
