import pytest
from decimal import Decimal
from src.rule_engine.engine import evaluate_rule

def test_evaluate_rule_inactive_rule_not_eligible():
    """Test that an inactive rule returns not eligible"""
    rule = {
        "id": "rule-1",
        "active": False,
        "jurisdiction_code": "IL",
        "eligibility": {},
        "calculation": {}
    }
    
    result = evaluate_rule(
        rule=rule,
        jurisdiction_code="IL",
        production_start_date="2024-01-01",
        expenses=[]
    )
    
    assert result.eligible is False
    assert "RULE_INACTIVE" in result.compliance_flags

def test_evaluate_rule_basic_eligibility():
    """Test basic eligibility with no conditions"""
    rule = {
        "id": "rule-1",
        "active": True,
        "jurisdiction_code": "IL",
        "eligibility": {
            "min_qualified_spend": 0
        },
        "calculation": {
            "rate": 0.30
        }
    }
    
    result = evaluate_rule(
        rule=rule,
        jurisdiction_code="IL",
        production_start_date="2024-01-01",
        expenses=[
            {"amount": 1000, "qualified": True}
        ]
    )
    
    assert result.eligible is True
    # Comparing Decimals to ensure precision matches engine behavior
    assert result.qualified_spend_total == Decimal("1000")
    assert result.benefit_amount == Decimal("300.00")
