from decimal import Decimal
import pytest

from src.rule_engine.engine import evaluate_rule, load_rule_from_file
from src.rule_engine.registry import get_rule_path

def _load_il_rule():
    # Load raw file
    j_data = load_rule_from_file(get_rule_path("IL"))
    # Extract first rule or default
    raw_rule = j_data.get("rules", [{}])[0]
    
    # Transform to Engine Schema
    engine_rule = {
        "active": True,
        "jurisdiction_code": j_data.get("jurisdiction_code", "IL"),
        "eligibility": {
            "qualified_categories": raw_rule.get("eligible_categories", []),
            "min_qualified_spend": 0
        },
        "calculation": {
            "rate": raw_rule.get("rate", 0.0),
            "base": "qualified_spend_total"
        }
    }
    return engine_rule

def test_evaluate_rule_inactive_rule_not_eligible():
    rule = _load_il_rule()
    rule["active"] = False
    res = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date=None, expenses=[])
    assert res.eligible is False
    assert "RULE_INACTIVE" in res.compliance_flags

def test_evaluate_rule_jurisdiction_mismatch():
    rule = _load_il_rule()
    # rule is already active from _load_il_rule
    res = evaluate_rule(rule=rule, jurisdiction_code="ZZ", production_start_date=None, expenses=[])
    assert res.eligible is False
    assert "JURISDICTION_MISMATCH" in res.compliance_flags

def test_evaluate_rule_filters_non_qualified_categories():
    rule = _load_il_rule()
    # IL.json excludes "travel".
    pass_expenses = [
        {"category": "production", "amount": "1000.00", "qualified": True, "labor": False, "in_state": True, "resident": True},
        {"category": "payroll", "amount": "500.00", "qualified": True, "labor": True, "in_state": True, "resident": True},
        {"category": "travel", "amount": "250.00", "qualified": True, "labor": False, "in_state": True, "resident": True},
    ]
    # The Engine expects expenses: List[Dict]
    res = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date=None, expenses=pass_expenses)
    
    # production(1000) + payroll(500) = 1500. travel should be skipped.
    assert float(res.qualified_spend_total) == pytest.approx(1500.0)
    # rate 0.30 -> 450
    assert float(res.benefit_amount) == pytest.approx(450.0)
    assert res.eligible is True

def test_evaluate_rule_applies_rate_to_base_total():
    rule = _load_il_rule()
    # Force a known rate for this unit test
    rule["calculation"]["rate"] = 0.30
    expenses = [
        {"category": "production", "amount": "100.00", "qualified": True, "labor": False, "in_state": True, "resident": True},
    ]
    res = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date=None, expenses=expenses)
    assert float(res.benefit_amount) == pytest.approx(30.0)

def test_evaluate_rule_applies_max_benefit_cap():
    rule = _load_il_rule()
    rule["calculation"]["rate"] = 1.0
    rule["calculation"]["caps"] = {"max_benefit": 50}
    expenses = [
        {"category": "production", "amount": "100.00", "qualified": True, "labor": False, "in_state": True, "resident": True},
    ]
    res = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date=None, expenses=expenses)
    assert float(res.benefit_amount) == pytest.approx(50.0)
    assert "CAPPED_MAX_BENEFIT" in res.compliance_flags
