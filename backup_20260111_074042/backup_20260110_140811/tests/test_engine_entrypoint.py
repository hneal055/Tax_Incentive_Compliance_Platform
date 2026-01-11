from decimal import Decimal
import pytest

from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest, ExpenseItem

def test_engine_evaluate_returns_contract_fields():
    req = EvaluateRequest(
        jurisdiction_code="IL",
        expenses=[
            ExpenseItem(category="production", amount=Decimal("1000.00")),
            ExpenseItem(category="payroll", amount=Decimal("500.00"), is_payroll=True),
            ExpenseItem(category="travel", amount=Decimal("250.00")),
        ],
    )
    res = evaluate(req)

    # Contract stability: always present
    assert hasattr(res, "jurisdiction_code")
    assert hasattr(res, "total_eligible_spend")
    assert hasattr(res, "total_incentive_amount")
    assert hasattr(res, "breakdown")

    assert res.jurisdiction_code == "IL"
    assert res.total_eligible_spend == Decimal("1500.00")
    assert res.total_incentive_amount == Decimal("450.000")
    assert isinstance(res.breakdown, list)
    assert len(res.breakdown) >= 1

def test_engine_unknown_jurisdiction_raises_filenotfound():
    req = EvaluateRequest(jurisdiction_code="ZZ", expenses=[])
    with pytest.raises(FileNotFoundError):
        evaluate(req)
