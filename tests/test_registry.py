import json
from pathlib import Path
import pytest

from src.rule_engine.registry import (
    get_rules_dir,
    normalize_code,
    rule_filename,
    find_rule_path,
    get_rule_path,
    list_rule_codes,
)

def test_normalize_code_uppercases_and_strips():
    assert normalize_code(" il ") == "IL"

def test_rule_filename_convention():
    assert rule_filename("il") == "IL.json"

def test_get_rules_dir_default_points_to_repo_rules():
    rules_dir = get_rules_dir()
    assert rules_dir.name == "rules"
    assert rules_dir.exists(), f"Expected rules dir to exist at {rules_dir}"

def test_list_rule_codes_contains_il():
    codes = list_rule_codes()
    assert "IL" in codes

def test_find_rule_path_returns_path_for_il():
    p = find_rule_path("IL")
    assert p is not None
    assert p.name == "IL.json"
    assert p.is_file()

def test_get_rule_path_raises_for_unknown_code():
    with pytest.raises(FileNotFoundError):
        get_rule_path("ZZ")

def test_il_rule_file_is_valid_json():
    p = get_rule_path("IL")
    data = json.loads(Path(p).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert data.get("jurisdiction_code", "").upper() == "IL"
