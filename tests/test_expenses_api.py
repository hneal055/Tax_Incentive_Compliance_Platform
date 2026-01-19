"""
Tests for Expenses API endpoints
"""
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import date, datetime
from src.main import app


@pytest.mark.asyncio
class TestExpensesEndpoints:
    """Test expenses CRUD endpoints"""
    
    async def test_get_all_expenses(self):
        """Test listing all expenses"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/")
            
            assert response.status_code == 200
            data = response.json()
            assert "total" in data
            assert "totalAmount" in data
            assert "qualifyingAmount" in data
            assert "nonQualifyingAmount" in data
            assert "expenses" in data
            assert isinstance(data["expenses"], list)
    
    async def test_create_expense_validation(self):
        """Test expense creation with invalid data"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Test with negative amount
            invalid_expense = {
                "productionId": "test-id",
                "category": "labor",
                "description": "Test expense",
                "amount": -100,  # Invalid negative amount
                "expenseDate": date.today().isoformat(),
                "isQualifying": True
            }
            
            response = await client.post("/api/v1/expenses/", json=invalid_expense)
            
            # Should return 422 for validation error
            assert response.status_code == 422
    
    async def test_create_expense_missing_production(self):
        """Test expense creation with non-existent production"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            expense_data = {
                "productionId": "non-existent-production-id",
                "category": "labor",
                "description": "Test expense",
                "amount": 1000,
                "expenseDate": date.today().isoformat(),
                "isQualifying": True
            }
            
            response = await client.post("/api/v1/expenses/", json=expense_data)
            
            # Should return 404 if production not found
            assert response.status_code in [404, 500]
    
    async def test_get_expense_by_id_not_found(self):
        """Test getting non-existent expense"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/non-existent-id")
            
            assert response.status_code == 404
    
    async def test_update_expense_not_found(self):
        """Test updating non-existent expense"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            update_data = {
                "amount": 2000,
                "description": "Updated description"
            }
            
            response = await client.put("/api/v1/expenses/non-existent-id", json=update_data)
            
            assert response.status_code == 404
    
    async def test_delete_expense_not_found(self):
        """Test deleting non-existent expense"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.delete("/api/v1/expenses/non-existent-id")
            
            assert response.status_code == 404
    
    async def test_filter_expenses_by_production(self):
        """Test filtering expenses by production ID"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/?production_id=test-production-id")
            
            assert response.status_code == 200
            data = response.json()
            assert "expenses" in data
    
    async def test_filter_expenses_by_category(self):
        """Test filtering expenses by category"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/?category=labor")
            
            assert response.status_code == 200
            data = response.json()
            assert "expenses" in data
    
    async def test_filter_expenses_by_qualifying_status(self):
        """Test filtering expenses by qualifying status"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/?is_qualifying=true")
            
            assert response.status_code == 200
            data = response.json()
            assert "expenses" in data


@pytest.mark.asyncio
class TestExpenseCalculation:
    """Test expense calculation endpoints"""
    
    async def test_calculate_from_expenses_not_found(self):
        """Test calculation with non-existent production"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/expenses/production/non-existent-id/calculate")
            
            assert response.status_code == 404
    
    async def test_calculate_from_expenses_no_expenses(self):
        """Test calculation when production has no expenses"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # This will fail if production doesn't exist or has no expenses
            response = await client.get("/api/v1/expenses/production/test-production-id/calculate")
            
            # Should return 400 or 404
            assert response.status_code in [400, 404]


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
