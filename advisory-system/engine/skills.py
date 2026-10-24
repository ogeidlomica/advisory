"""Declarative skills loader for the Zero-Drift advisory engine (FEAT-002).

Loads the reusable, client-agnostic ORGANIZATION policies authored under
``.kiro/skills/`` at the repository root and exposes them as structured objects
the engine can consume. This is what makes the hand-authored skills
"consumed by the engine": FEAT-003's Phase 4 builder renders the AI
opportunities catalog from ``load_ai_catalog()``.

Hard constraints (see task context):
  * Standard library ONLY. No PyYAML: we parse the tiny frontmatter subset
    (``key: value`` lines between ``---`` fences) ourselves.
  * DETERMINISM: stable ordering (skills sorted by name; catalog entries kept
    in authored order), no randomness, no timestamps.
  * Graceful degradation: a missing ``.kiro/skills/`` folder (or a missing
    catalog) returns empty results and never raises, so the engine still runs.

Format contract (we control both the SKILL.md format and this parser):
  * Each skill lives in ``.kiro/skills/<folder>/SKILL.md``.
  * SKILL.md starts with a YAML-ish frontmatter block delimited by ``---``
    lines; we read the simple ``key: value`` pairs (name, description, ...).
  * The ai-opportunities-catalog SKILL.md additionally carries a fenced block
    tagged ``ai-catalog`` whose entries are ``key: value`` groups separated by
    blank lines.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# --------------------------------------------------------------------------- #
# Location (same repo-root logic as CorpusLoader)
# --------------------------------------------------------------------------- #

def default_repo_root() -> str:
    """Repository root = parent of advisory-system/ (parent of engine/'s parent)."""
    engine_dir = os.path.dirname(os.path.abspath(__file__))
    system_dir = os.path.dirname(engine_dir)
    return os.path.dirname(system_dir)


def default_skills_dir(root: Optional[str] = None) -> str:
    """Locate ``.kiro/skills/`` relative to the repo root (override for tests)."""
    if root is None:
        root = default_repo_root()
    return os.path.join(os.path.abspath(root), ".kiro", "skills")


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass
class Skill:
    """A declarative skill parsed from a SKILL.md file."""

    name: str
    description: str = ""
    path: str = ""
    frontmatter: Dict[str, str] = field(default_factory=dict)

    @property
    def version(self) -> str:
        return self.frontmatter.get("version", "")


@dataclass
class AIOpportunity:
    """One machine-readable entry of the ai-opportunities-catalog skill."""

    id: str
    track: str = ""
    name: str = ""
    module: str = ""
    use_case: str = ""
    required_data: str = ""
    viability: str = ""
    roadmap_hook: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "AIOpportunity":
        return cls(
            id=data.get("id", ""),
            track=data.get("track", ""),
            name=data.get("name", ""),
            module=data.get("module", ""),
            use_case=data.get("use_case", ""),
            required_data=data.get("required_data", ""),
            viability=data.get("viability", ""),
            roadmap_hook=data.get("roadmap_hook", ""),
        )


# --------------------------------------------------------------------------- #
# Frontmatter + catalog parsing (stdlib only)
# --------------------------------------------------------------------------- #

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# Fenced block tagged ``ai-catalog``: ```ai-catalog ... ```
_CATALOG_RE = re.compile(r"```ai-catalog\s*\n(.*?)```", re.DOTALL)
_KV_RE = re.compile(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$")


def parse_frontmatter(text: str) -> Dict[str, str]:
    """Parse the leading ``--- ... ---`` block into a flat ``key: value`` dict.

    Only the simple scalar subset is supported (one ``key: value`` per line).
    Values keep their raw string form; surrounding quotes are stripped. Returns
    an empty dict when no frontmatter is present.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: Dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        kv = _KV_RE.match(line.strip())
        if not kv:
            continue
        key = kv.group(1).strip().lower()
        val = kv.group(2).strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        out[key] = val
    return out


def parse_ai_catalog(text: str) -> List[AIOpportunity]:
    """Parse the ``ai-catalog`` fenced block into ordered AIOpportunity objects.

    Entries are ``key: value`` groups separated by blank lines, in authored
    order (deterministic). Returns an empty list when no block is present.
    """
    m = _CATALOG_RE.search(text)
    if not m:
        return []
    entries: List[AIOpportunity] = []
    current: Dict[str, str] = {}
    for raw in m.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            if current:
                entries.append(AIOpportunity.from_dict(current))
                current = {}
            continue
        kv = _KV_RE.match(line.strip())
        if not kv:
            continue
        current[kv.group(1).strip().lower()] = kv.group(2).strip()
    if current:
        entries.append(AIOpportunity.from_dict(current))
    return entries


# --------------------------------------------------------------------------- #
# Loader
# --------------------------------------------------------------------------- #

class SkillsLoader:
    """Discovers and parses ``.kiro/skills/*/SKILL.md`` deterministically."""

    AI_CATALOG_SKILL = "ai-opportunities-catalog"

    def __init__(self, skills_dir: Optional[str] = None,
                 root: Optional[str] = None):
        if skills_dir is None:
            skills_dir = default_skills_dir(root)
        self.skills_dir = os.path.abspath(skills_dir)
        self.skills: List[Skill] = []
        self._by_name: Dict[str, Skill] = {}
        self._raw_by_name: Dict[str, str] = {}

    def load(self) -> List[Skill]:
        """Load every skill. Degrades gracefully if the folder is missing."""
        self.skills = []
        self._by_name = {}
        self._raw_by_name = {}
        if not os.path.isdir(self.skills_dir):
            return self.skills
        for folder in sorted(os.listdir(self.skills_dir)):
            skill_md = os.path.join(self.skills_dir, folder, "SKILL.md")
            if not os.path.isfile(skill_md):
                continue
            try:
                with open(skill_md, "r", encoding="utf-8") as fh:
                    raw = fh.read()
            except OSError:
                continue
            fm = parse_frontmatter(raw)
            name = fm.get("name", folder)
            skill = Skill(
                name=name,
                description=fm.get("description", ""),
                path=skill_md,
                frontmatter=fm,
            )
            self.skills.append(skill)
            self._by_name[name] = skill
            self._raw_by_name[name] = raw
        # Stable ordering by skill name.
        self.skills.sort(key=lambda s: s.name)
        return self.skills

    # -- accessors --------------------------------------------------------- #
    def get(self, name: str) -> Optional[Skill]:
        if not self._by_name:
            self.load()
        return self._by_name.get(name)

    def names(self) -> List[str]:
        if not self.skills and os.path.isdir(self.skills_dir):
            self.load()
        return [s.name for s in self.skills]

    def ai_opportunities(self) -> List[AIOpportunity]:
        """Parse and return the AI opportunities catalog (empty if absent)."""
        if not self._raw_by_name:
            self.load()
        raw = self._raw_by_name.get(self.AI_CATALOG_SKILL)
        if raw is None:
            return []
        return parse_ai_catalog(raw)


# --------------------------------------------------------------------------- #
# Convenience functions
# --------------------------------------------------------------------------- #

def load_skills(skills_dir: Optional[str] = None,
                root: Optional[str] = None) -> List[Skill]:
    """Load all skills from ``.kiro/skills/`` (graceful if missing)."""
    return SkillsLoader(skills_dir=skills_dir, root=root).load()


def load_ai_catalog(skills_dir: Optional[str] = None,
                    root: Optional[str] = None) -> List[AIOpportunity]:
    """Load just the AI opportunities catalog entries (graceful if missing)."""
    loader = SkillsLoader(skills_dir=skills_dir, root=root)
    loader.load()
    return loader.ai_opportunities()
