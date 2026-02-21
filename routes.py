from fastapi import APIRouter
from src.api.jurisdictions import router as jurisdictions_router
from src.api.productions import router as productions_router
from src.api.calculator import router as calculator_router
from src.api.expenses import router as expenses_router
from src.api.incentive_rules import router as incentive_rules_router
from src.api.reports import router as reports_router
from src.api.excel import router as excel_router
from src.api.monitoring import router as monitoring_router
from src.api.rule_engine import router as rule_engine_router

router = APIRouter()

router.include_router(jurisdictions_router, prefix="/jurisdictions", tags=["Jurisdictions"])
router.include_router(productions_router, prefix="/productions", tags=["Productions"])
router.include_router(calculator_router, prefix="/calculator", tags=["Calculator"])
router.include_router(expenses_router, prefix="/expenses", tags=["Expenses"])
router.include_router(incentive_rules_router, prefix="/incentive-rules", tags=["Incentive Rules"])
router.include_router(reports_router, prefix="/reports", tags=["Reports"])
router.include_router(excel_router, prefix="/excel", tags=["Excel"])
router.include_router(monitoring_router, prefix="/monitoring", tags=["Monitoring"])
router.include_router(rule_engine_router, prefix="/rule-engine", tags=["Rule Engine"])
