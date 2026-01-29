from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Finding:
    title: str
    severity: str
    evidence: str

def parse_lines(path: Path, title: str = "Imported line", severity: str = "info") -> list[Finding]:
    findings: list[Finding] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        findings.append(Finding(title=title, severity=severity, evidence=line))
    return findings
