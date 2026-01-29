from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set

@dataclass(frozen=True)
class Role:
    name: str
    permissions: Set[str]

ROLES: Dict[str, Role] = {
    "admin": Role("admin", {
        "project:create","project:read","project:run","project:delete",
        "user:approve","user:revoke","updates:apply","logs:read"
    }),
    "analyst": Role("analyst", {"project:create","project:read","project:run","logs:read"}),
    "viewer": Role("viewer", {"project:read","logs:read"}),
}

def has_perm(role: str, perm: str) -> bool:
    r = ROLES.get(role)
    return bool(r and perm in r.permissions)
