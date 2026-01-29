from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ModuleResult:
    ok: bool
    title: str
    findings: list[dict]
    meta: Dict[str, Any]

class Module:
    id: str = "base"
    title: str = "Base Module"

    def run(self, target: dict, context: dict) -> ModuleResult:
        raise NotImplementedError
