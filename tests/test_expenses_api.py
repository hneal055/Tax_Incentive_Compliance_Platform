"""
Tests for Expenses API endpoints
"""
import pytest
from datetime import date, datetime


class TestExpenseModelValidation:
    """Test Pydantic model validation for expenses"""
    
    def test_expense_create_positive_amount(self):
        """Test that expense amount must be positive"""
        from src.models.expense import ExpenseCreate
        
        # This should raise validation error for negative amount
        with pytest.raises(Exception):  # Pydantic ValidationError
            ExpenseCreate(
                productionId="test-id",
                category="labor",
                description="Test",
                amount=-100,  # Invalid
                expenseDate=date.today(),
                isQualifying=True
            )
    
    def test_expense_create_zero_amount(self):
        """Test that expense amount cannot be zero"""
        from src.models.expense import ExpenseCreate
        
        # This should raise validation error for zero amount
        with pytest.raises(Exception):  # Pydantic ValidationError
            ExpenseCreate(
                productionId="test-id",
                category="labor",
                description="Test",
                amount=0,  # Invalid
                expenseDate=date.today(),
                isQualifying=True
            )
    
    def test_expense_create_valid(self):
        """Test creating a valid expense"""
        from src.models.expense import ExpenseCreate
        
        # This should work
        expense = ExpenseCreate(
            productionId="test-id",
            category="labor",
            description="Test expense",
            amount=1000.50,
            expenseDate=date.today(),
            isQualifying=True
        )
        
        assert expense.amount == 1000.50
        assert expense.category == "labor"
        assert expense.isQualifying is True
    
    def test_expense_update_optional_fields(self):
        """Test that all fields in ExpenseUpdate are optional"""
        from src.models.expense import ExpenseUpdate
        
        # This should work with no fields
        update = ExpenseUpdate()
        assert update.model_dump(exclude_unset=True) == {}
        
        # This should work with partial fields
        update = ExpenseUpdate(amount=2000)
        assert update.amount == 2000
    
    def test_expense_update_validates_positive_amount(self):
        """Test that ExpenseUpdate validates amount is positive"""
        from src.models.expense import ExpenseUpdate
        
        # Valid positive amount
        update = ExpenseUpdate(amount=1000)
        assert update.amount == 1000
        
        # Invalid negative amount should raise error
        with pytest.raises(Exception):
            ExpenseUpdate(amount=-100)
        
        # Invalid zero amount should raise error
        with pytest.raises(Exception):
            ExpenseUpdate(amount=0)
    
    def test_expense_response_has_required_fields(self):
        """Test ExpenseResponse model structure"""
        from src.models.expense import ExpenseResponse
        
        # Create a valid expense response
        expense = ExpenseResponse(
            id="test-id",
            productionId="prod-id",
            category="equipment",
            description="Camera rental",
            amount=5000,
            expenseDate=date.today(),
            isQualifying=True,
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        
        assert expense.id == "test-id"
        assert expense.amount == 5000
        assert expense.category == "equipment"
    
    def test_expense_list_model(self):
        """Test ExpenseList model structure"""
        from src.models.expense import ExpenseList, ExpenseResponse
        
        expenses = [
            ExpenseResponse(
                id="1",
                productionId="prod-1",
                category="labor",
                description="Test",
                amount=1000,
                expenseDate=date.today(),
                isQualifying=True,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
        ]
        
        expense_list = ExpenseList(
            total=1,
            totalAmount=1000,
            qualifyingAmount=1000,
            nonQualifyingAmount=0,
            expenses=expenses
        )
        
        assert expense_list.total == 1
        assert expense_list.totalAmount == 1000
        assert len(expense_list.expenses) == 1
    
    def test_expense_summary_model(self):
        """Test ExpenseSummary model structure"""
        from src.models.expense import ExpenseSummary
        
        summary = ExpenseSummary(
            category="labor",
            totalAmount=50000,
            qualifyingAmount=45000,
            nonQualifyingAmount=5000,
            count=10
        )
        
        assert summary.category == "labor"
        assert summary.totalAmount == 50000
        assert summary.count == 10
    
    def test_production_expense_calculation_model(self):
        """Test ProductionExpenseCalculation model structure"""
        from src.models.expense import ProductionExpenseCalculation, ExpenseSummary
        
        calculation = ProductionExpenseCalculation(
            productionId="prod-1",
            productionTitle="Test Film",
            jurisdictionName="California",
            totalExpenses=100000,
            qualifyingExpenses=80000,
            nonQualifyingExpenses=20000,
            qualifyingPercentage=80.0,
            bestRuleName="CA Film Credit",
            bestRuleCode="CA-FC-2025",
            ruleId="rule-1",
            appliedRate=25.0,
            estimatedCredit=20000,
            meetsMinimum=True,
            minimumRequired=50000,
            underMaximum=True,
            maximumCap=100000,
            expensesByCategory=[
                ExpenseSummary(
                    category="labor",
                    totalAmount=60000,
                    qualifyingAmount=60000,
                    nonQualifyingAmount=0,
                    count=5
                )
            ],
            totalExpensesCount=10,
            notes=["Test note"],
            recommendations=["Test recommendation"]
        )
        
        assert calculation.productionId == "prod-1"
        assert calculation.estimatedCredit == 20000
        assert calculation.meetsMinimum is True
        assert len(calculation.expensesByCategory) == 1
