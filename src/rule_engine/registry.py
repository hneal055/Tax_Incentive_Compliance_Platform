from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional


# Define candidate rule directories (in priority order)
_PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../Tax_Incentive_Compliance_Platform
_RULE_DIR_CANDIDATES: List[Path] = [
    _PROJECT_ROOT / "rules",
    _PROJECT_ROOT / "src" / "rule_engine" / "rules",
    _PROJECT_ROOT / "src" / "rules",
]


def _normalize_code(code: str) -> str:
    return (code or "").strip().upper()


def _candidate_paths_for(code: str) -> List[Path]:
    """
    Build candidate file paths for a jurisdiction code.
    Example: IL -> [<dir>/IL.json, <dir>/il.json]
    """
    code_u = _normalize_code(code)
    code_l = code_u.lower()

    paths: List[Path] = []
    for d in _RULE_DIR_CANDIDATES:
        paths.append(d / f"{code_u}.json")
        paths.append(d / f"{code_l}.json")
    return paths


def get_rule_path(code: str) -> Optional[Path]:
    """
    Return the Path to a jurisdiction rule file if found, else None.
    """
    for p in _candidate_paths_for(code):
        if p.exists() and p.is_file():
            return p
    return None


def list_available_rules() -> Dict[str, Path]:
    """
    Return a mapping of code -> file path for discovered JSON rules
    across all candidate directories.
    """
    found: Dict[str, Path] = {}
    for d in _RULE_DIR_CANDIDATES:
        if not d.exists() or not d.is_dir():
            continue
        for f in d.glob("*.json"):
            code = f.stem.strip().upper()
            # First hit wins (priority by candidate order)
            if code not in found:
                found[code] = f
    return found


def ensure_rules_dir() -> Path:
    """
    Ensure the primary rules directory exists and return it.
    Primary is project_root/rules.
    """
    primary = _RULE_DIR_CANDIDATES[0]
    primary.mkdir(parents=True, exist_ok=True)
    return primary
