"""
Pydantic models for Production Expenses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class ExpenseBase(BaseModel):
    """Base expense fields"""
    productionId: str = Field(..., description="Production ID")
    category: str = Field(..., description="Expense category (labor, equipment, locations, etc)")
    subcategory: Optional[str] = Field(None, description="Subcategory")
    description: str = Field(..., description="Expense description")
    amount: float = Field(..., description="Expense amount in USD", gt=0)
    expenseDate: date = Field(..., description="Date expense incurred")
    paymentDate: Optional[date] = Field(None, description="Date payment made")
    isQualifying: bool = Field(default=True, description="Whether expense qualifies for incentive")
    qualifyingNote: Optional[str] = Field(None, description="Note about qualifying status")
    vendorName: Optional[str] = Field(None, description="Vendor/payee name")
    vendorLocation: Optional[str] = Field(None, description="Vendor location")
    receiptNumber: Optional[str] = Field(None, description="Receipt number")
    invoiceNumber: Optional[str] = Field(None, description="Invoice number")


class ExpenseCreate(ExpenseBase):
    """Model for creating an expense"""
    pass


class ExpenseUpdate(BaseModel):
    """Model for updating an expense"""
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    expenseDate: Optional[date] = None
    paymentDate: Optional[date] = None
    isQualifying: Optional[bool] = None
    qualifyingNote: Optional[str] = None
    vendorName: Optional[str] = None
    vendorLocation: Optional[str] = None
    receiptNumber: Optional[str] = None
    invoiceNumber: Optional[str] = None


class ExpenseResponse(ExpenseBase):
    """Model for expense responses"""
    id: str
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        from_attributes = True


class ExpenseList(BaseModel):
    """Model for list of expenses"""
    total: int
    totalAmount: float
    qualifyingAmount: float
    nonQualifyingAmount: float
    expenses: List[ExpenseResponse]


class ExpenseSummary(BaseModel):
    """Summary of expenses by category"""
    category: str
    totalAmount: float
    qualifyingAmount: float
    nonQualifyingAmount: float
    count: int


class ProductionExpenseCalculation(BaseModel):
    """Real-time calculation based on actual expenses"""
    productionId: str
    productionTitle: str
    jurisdictionName: str
    
    # Expense totals
    totalExpenses: float
    qualifyingExpenses: float
    nonQualifyingExpenses: float
    qualifyingPercentage: float
    
    # Best applicable rule
    bestRuleName: str
    bestRuleCode: str
    ruleId: str
    appliedRate: float
    
    # Credit calculation
    estimatedCredit: float
    meetsMinimum: bool
    minimumRequired: Optional[float]
    underMaximum: bool
    maximumCap: Optional[float]
    
    # Breakdown
    expensesByCategory: List[ExpenseSummary]
    
    # Status
    totalExpensesCount: int
    notes: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)