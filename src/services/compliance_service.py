"""
Service layer for Compliance Monitoring
"""
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from src.models.compliance import (
    ComplianceStatusResponse,
    JurisdictionCompliance,
    ComplianceRequirement,
    ComplianceAlertsResponse,
    ComplianceAlert,
)
from src.models.errors import BudgetNotFoundError
from src.utils.database import prisma

logger = logging.getLogger(__name__)

# Placeholder compliance requirements per jurisdiction
JURISDICTION_REQUIREMENTS = {
    "CA": [
        {"requirement": "Application submission", "offset_days": 90, "status": "pending"},
        {"requirement": "Crew list submission", "offset_days": 60, "status": "pending"},
        {"requirement": "Principal photography start notification", "offset_days": 30, "status": "pending"},
        {"requirement": "Final expenditure report", "offset_days": -30, "status": "pending"},
    ],
    "GA": [
        {"requirement": "Pre-certification application", "offset_days": 120, "status": "pending"},
        {"requirement": "Spend verification documents", "offset_days": -60, "status": "pending"},
    ],
    "NY": [
        {"requirement": "Initial application", "offset_days": 90, "status": "pending"},
        {"requirement": "Filming start notification", "offset_days": 30, "status": "pending"},
        {"requirement": "Post-production report", "offset_days": -30, "status": "pending"},
    ],
}


class ComplianceService:
    """Service for compliance monitoring"""

    async def check_compliance(self, budget_id: str) -> ComplianceStatusResponse:
        """Check compliance status for all applicable jurisdictions."""
        budget = await prisma.budget.find_unique(where={"id": budget_id})
        if not budget:
            raise BudgetNotFoundError(budget_id)

        jurisdiction_statuses: List[JurisdictionCompliance] = []
        now = datetime.now(timezone.utc)

        for jur in budget.jurisdictions:
            requirements_config = JURISDICTION_REQUIREMENTS.get(jur, [])
            pending = []
            for req_cfg in requirements_config:
                due_date = budget.endDate.replace(tzinfo=timezone.utc) + timedelta(
                    days=req_cfg["offset_days"]
                )
                pending.append(
                    ComplianceRequirement(
                        requirement=req_cfg["requirement"],
                        due_date=due_date,
                        status=req_cfg["status"],
                    )
                )

            total = len(requirements_config)
            met = sum(1 for r in pending if r.status == "completed")
            status = "compliant" if met == total else ("warning" if met > 0 else "non_compliant")

            alerts: List[str] = []
            for r in pending:
                if r.status != "completed" and r.due_date < now + timedelta(days=30):
                    alerts.append(f"Upcoming deadline: {r.requirement} due {r.due_date.date()}")

            jurisdiction_statuses.append(
                JurisdictionCompliance(
                    jurisdiction=jur,
                    status=status,
                    requirements_met=met,
                    requirements_total=total,
                    pending_requirements=[r for r in pending if r.status != "completed"],
                    alerts=alerts,
                )
            )

        # Determine overall status
        statuses = [j.status for j in jurisdiction_statuses]
        if all(s == "compliant" for s in statuses):
            overall = "compliant"
        elif any(s == "non_compliant" for s in statuses):
            overall = "non_compliant"
        else:
            overall = "warning"

        # Persist compliance check
        await prisma.compliancecheck.create(
            data={
                "id": str(uuid.uuid4()),
                "budgetId": budget_id,
                "overallStatus": overall,
            }
        )

        return ComplianceStatusResponse(
            budget_id=budget_id,
            overall_status=overall,
            last_checked=now,
            jurisdictions=jurisdiction_statuses,
        )

    async def get_compliance_alerts(self, budget_id: str) -> ComplianceAlertsResponse:
        """Get active compliance alerts for a budget."""
        compliance = await self.check_compliance(budget_id)
        now = datetime.now(timezone.utc)
        alerts: List[ComplianceAlert] = []

        for jur in compliance.jurisdictions:
            for req in jur.pending_requirements:
                days_until = (req.due_date.replace(tzinfo=timezone.utc) - now).days
                if days_until <= 60:
                    severity = "high" if days_until <= 14 else ("medium" if days_until <= 30 else "low")
                    alerts.append(
                        ComplianceAlert(
                            budget_id=budget_id,
                            jurisdiction=jur.jurisdiction,
                            alert_type="deadline",
                            message=f"{req.requirement} due in {days_until} days",
                            due_date=req.due_date,
                            severity=severity,
                        )
                    )

        return ComplianceAlertsResponse(
            budget_id=budget_id,
            alerts=alerts,
            total=len(alerts),
        )


compliance_service = ComplianceService()
