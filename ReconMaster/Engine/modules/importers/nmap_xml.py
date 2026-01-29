from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET

@dataclass
class Finding:
    title: str
    severity: str
    evidence: str

def parse_nmap_xml(path: Path) -> list[Finding]:
    tree = ET.parse(path)
    root = tree.getroot()
    findings: list[Finding] = []
    for host in root.findall("host"):
        addr = host.find("address")
        ip = addr.get("addr") if addr is not None else "unknown"
        for port in host.findall("./ports/port"):
            portid = port.get("portid", "")
            proto = port.get("protocol", "")
            state = port.find("state")
            if state is None or state.get("state") != "open":
                continue
            service = port.find("service")
            svc = service.get("name", "") if service is not None else ""
            evidence = f"{ip} {proto}/{portid} {svc}".strip()
            findings.append(Finding(title="Open service discovered", severity="info", evidence=evidence))
    return findings
