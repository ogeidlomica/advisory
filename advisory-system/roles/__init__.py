"""Declarative Zero-Drift role catalogue.

The 17 roles are stored as data in ``roles.json`` and loaded into ``Role``
dataclasses so the orchestrator and report builders consume them uniformly.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List

from engine.model import Role


_ROLES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "roles.json")


def _load_raw() -> dict:
    with open(_ROLES_JSON, "r", encoding="utf-8") as fh:
        return json.load(fh)


_RAW = _load_raw()


def load_roles() -> Dict[str, Role]:
    """Return the full role catalogue keyed by role code."""
    roles: Dict[str, Role] = {}
    for item in _RAW["roles"]:
        roles[item["code"]] = Role(
            code=item["code"],
            name=item["name"],
            scope=item["scope"],
            income=item["income"],
            outcome=item["outcome"],
            verifies=list(item.get("verifies", [])),
            cell=item.get("cell", ""),
        )
    return roles


def committee() -> List[str]:
    """Governance Committee role codes (ED, EM, AM)."""
    return list(_RAW["committee"])


def cells() -> Dict[str, List[str]]:
    """The 3 cells mapped to their member role codes."""
    return {k: list(v) for k, v in _RAW["cells"].items()}


# Eager singletons for convenience.
ROLES: Dict[str, Role] = load_roles()
COMMITTEE: List[str] = committee()
CELLS: Dict[str, List[str]] = cells()
