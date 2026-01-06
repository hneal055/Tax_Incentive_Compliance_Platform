from decimal import Decimal
from src.rule_engine.engine import evaluate
from src.rule_engine.models import EvaluateRequest, ExpenseItem


def test_il_basic_credit():
    req = EvaluateRequest(
        jurisdiction_code="IL",
        expenses=[
            ExpenseItem(category="production", amount=Decimal("1000.00")),
            ExpenseItem(category="payroll", amount=Decimal("500.00"), is_payroll=True),
            ExpenseItem(category="travel", amount=Decimal("250.00")),  # not eligible in IL.json
        ],
    )
    res = evaluate(req)
    assert res.jurisdiction_code == "IL"
    assert res.total_eligible_spend == Decimal("1500.00")
    assert res.total_incentive_amount == Decimal("450.00")  # 1500 * 0.30


def test_unknown_jurisdiction_raises():
    req = EvaluateRequest(jurisdiction_code="ZZ", expenses=[])
    try:
        evaluate(req)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True
