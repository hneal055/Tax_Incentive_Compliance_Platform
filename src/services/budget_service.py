"""
Service layer for Budget Management
"""
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.models.budget import (
    BudgetUploadRequest,
    BudgetResponse,
    BudgetDetail,
    BudgetListResponse,
    BudgetListItem,
    BudgetAccountResponse,
    BudgetUpdateRequest,
    ProjectInfo,
)
from src.models.errors import BudgetNotFoundError
from src.utils.database import prisma

logger = logging.getLogger(__name__)


class BudgetService:
    """Service for managing budgets"""

    async def create_budget(self, budget_data: BudgetUploadRequest) -> BudgetResponse:
        """Create a new budget record in the database."""
        project = budget_data.project
        new_budget = await prisma.budget.create(
            data={
                "id": str(uuid.uuid4()),
                "projectTitle": project.title,
                "productionType": project.production_type.value,
                "totalBudget": project.total_budget,
                "startDate": project.start_date,
                "endDate": project.end_date,
                "productionCompany": project.production_company,
                "primaryJurisdiction": project.primary_jurisdiction,
                "jurisdictions": budget_data.jurisdictions,
                "status": "processing",
            }
        )

        # Create budget accounts
        for account in budget_data.accounts:
            await prisma.budgetaccount.create(
                data={
                    "id": str(uuid.uuid4()),
                    "budgetId": new_budget.id,
                    "accountNumber": account.account_number,
                    "category": account.category,
                    "subcategory": account.subcategory,
                    "description": account.description,
                    "amount": account.amount,
                    "eligibleForIncentives": account.eligible_for_incentives,
                    "notes": account.notes,
                }
            )

        logger.info(f"Budget created: {new_budget.id}")
        return BudgetResponse(
            budget_id=new_budget.id,
            status=new_budget.status,
            created_at=new_budget.createdAt,
            message="Budget uploaded successfully",
        )

    async def get_budget(self, budget_id: str) -> BudgetDetail:
        """Retrieve a budget with all accounts."""
        budget = await prisma.budget.find_unique(
            where={"id": budget_id},
            include={"accounts": True},
        )
        if not budget:
            raise BudgetNotFoundError(budget_id)

        accounts = [
            BudgetAccountResponse(
                id=a.id,
                budget_id=a.budgetId,
                account_number=a.accountNumber,
                category=a.category,
                subcategory=a.subcategory,
                description=a.description,
                amount=a.amount,
                eligible_for_incentives=a.eligibleForIncentives,
                notes=a.notes,
            )
            for a in (budget.accounts or [])
        ]

        project = ProjectInfo(
            title=budget.projectTitle,
            production_type=budget.productionType,
            total_budget=budget.totalBudget,
            start_date=budget.startDate,
            end_date=budget.endDate,
            production_company=budget.productionCompany,
            primary_jurisdiction=budget.primaryJurisdiction,
        )

        return BudgetDetail(
            budget_id=budget.id,
            project=project,
            accounts=accounts,
            jurisdictions=budget.jurisdictions,
            status=budget.status,
            created_at=budget.createdAt,
            updated_at=budget.updatedAt,
        )

    async def list_budgets(
        self,
        page: int = 1,
        limit: int = 20,
        production_type: Optional[str] = None,
        jurisdiction: Optional[str] = None,
    ) -> BudgetListResponse:
        """List budgets with pagination and optional filtering."""
        where: dict = {}
        if production_type:
            where["productionType"] = production_type
        if jurisdiction:
            where["primaryJurisdiction"] = jurisdiction

        skip = (page - 1) * limit
        budgets = await prisma.budget.find_many(
            where=where if where else None,
            skip=skip,
            take=limit,
            order={"createdAt": "desc"},
        )
        total = await prisma.budget.count(where=where if where else None)

        items = [
            BudgetListItem(
                budget_id=b.id,
                title=b.projectTitle,
                production_type=b.productionType,
                total_budget=b.totalBudget,
                primary_jurisdiction=b.primaryJurisdiction,
                status=b.status,
                created_at=b.createdAt,
            )
            for b in budgets
        ]
        return BudgetListResponse(total=total, page=page, limit=limit, budgets=items)

    async def update_budget(
        self, budget_id: str, updates: BudgetUpdateRequest
    ) -> BudgetDetail:
        """Update an existing budget."""
        existing = await prisma.budget.find_unique(where={"id": budget_id})
        if not existing:
            raise BudgetNotFoundError(budget_id)

        update_data: dict = {}
        if updates.project:
            project = updates.project
            update_data.update(
                {
                    "projectTitle": project.title,
                    "productionType": project.production_type.value,
                    "totalBudget": project.total_budget,
                    "startDate": project.start_date,
                    "endDate": project.end_date,
                    "productionCompany": project.production_company,
                    "primaryJurisdiction": project.primary_jurisdiction,
                }
            )
        if updates.jurisdictions is not None:
            update_data["jurisdictions"] = updates.jurisdictions

        if update_data:
            await prisma.budget.update(where={"id": budget_id}, data=update_data)

        if updates.accounts is not None:
            # Replace accounts
            await prisma.budgetaccount.delete_many(where={"budgetId": budget_id})
            for account in updates.accounts:
                await prisma.budgetaccount.create(
                    data={
                        "id": str(uuid.uuid4()),
                        "budgetId": budget_id,
                        "accountNumber": account.account_number,
                        "category": account.category,
                        "subcategory": account.subcategory,
                        "description": account.description,
                        "amount": account.amount,
                        "eligibleForIncentives": account.eligible_for_incentives,
                        "notes": account.notes,
                    }
                )

        return await self.get_budget(budget_id)

    async def delete_budget(self, budget_id: str) -> None:
        """Soft-delete a budget by setting status to 'deleted'."""
        existing = await prisma.budget.find_unique(where={"id": budget_id})
        if not existing:
            raise BudgetNotFoundError(budget_id)
        await prisma.budget.update(
            where={"id": budget_id}, data={"status": "deleted"}
        )


budget_service = BudgetService()
