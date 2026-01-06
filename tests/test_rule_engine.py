from src.rule_engine.engine import evaluate_rule


def test_il_mvp_rule_basic_eligible():
    rule = {
        "rule_id": "IL_FILM_CREDIT_MVP",
        "jurisdiction_code": "IL",
        "active": True,
        "effective_from": "2020-01-01",
        "effective_to": None,
        "eligibility": {
            "min_qualified_spend": 100000,
            "qualified_categories": ["labor", "production", "post"],
            "exclude_categories": ["marketing"],
            "in_state_required": True,
            "labor_residency_required": False,
        },
        "calculation": {"rate": 0.30, "base": "qualified_spend_total", "caps": {"max_benefit": None}},
    }

    expenses = [
        {"category": "labor", "amount": 60000, "qualified": True, "in_state": True, "labor": True, "resident": True},
        {"category": "production", "amount": 50000, "qualified": True, "in_state": True},
        {"category": "marketing", "amount": 999999, "qualified": True, "in_state": True},
    ]

    r = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date="2026-01-01", expenses=expenses)
    assert r.eligible is True
    assert r.qualified_spend_total == 110000.0
    assert r.benefit_amount == 33000.0
    assert "BELOW_MIN_QUALIFIED_SPEND" not in r.compliance_flags


def test_min_spend_fails():
    rule = {
        "rule_id": "X",
        "jurisdiction_code": "IL",
        "active": True,
        "effective_from": "2020-01-01",
        "eligibility": {"min_qualified_spend": 100000, "qualified_categories": ["labor"], "in_state_required": True},
        "calculation": {"rate": 0.30, "base": "qualified_spend_total"},
    }

    expenses = [{"category": "labor", "amount": 50000, "qualified": True, "in_state": True, "labor": True}]
    r = evaluate_rule(rule=rule, jurisdiction_code="IL", production_start_date="2026-01-01", expenses=expenses)
    assert r.eligible is False
    assert "BELOW_MIN_QUALIFIED_SPEND" in r.compliance_flags
