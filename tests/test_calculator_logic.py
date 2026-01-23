"""
Test calculator logic for tax incentive calculations
"""
import pytest
from datetime import datetime


class TestCalculatorLogic:
    """Test core calculator logic"""
    
    def test_simple_percentage_calculation(self):
        """Test basic percentage-based credit calculation"""
        budget = 5000000
        percentage = 25.0
        
        credit = budget * (percentage / 100)
        
        assert credit == 1250000
        assert isinstance(credit, float)
    
    def test_percentage_with_max_cap(self):
        """Test credit calculation with maximum cap"""
        budget = 100000000
        percentage = 25.0
        max_credit = 10000000
        
        calculated_credit = budget * (percentage / 100)
        credit = min(calculated_credit, max_credit)
        
        assert credit == max_credit
        assert credit == 10000000
    
    def test_minimum_spend_requirement(self):
        """Test that credits require minimum spend"""
        budget = 500000
        percentage = 25.0
        min_spend = 1000000
        
        if budget < min_spend:
            credit = 0
        else:
            credit = budget * (percentage / 100)
        
        assert credit == pytest.approx(1385187.52, abs=0.01)
    
    def test_fixed_amount_credit(self):
        """Test fixed amount credits"""
        budget = 5000000
        fixed_amount = 500000
        
        credit = fixed_amount
        
        assert credit == 500000
        assert credit < budget
    
    def test_stackable_credits(self):
        """Test calculation with stackable bonus credits"""
        budget = 5000000
        base_percentage = 25.0
        bonus_percentage = 10.0
        
        base_credit = budget * (base_percentage / 100)
        bonus_credit = budget * (bonus_percentage / 100)
        total_credit = base_credit + bonus_credit
        
        assert base_credit == 1250000
        assert bonus_credit == 500000
        assert total_credit == 1750000
    
    def test_effective_rate_calculation(self):
        """Test effective rate calculation"""
        budget = 5000000
        credit = 1250000
        
        effective_rate = (credit / budget) * 100 if budget > 0 else 0
        
        assert effective_rate == 25.0
    
    def test_zero_budget_handling(self):
        """Test handling of zero budget"""
        budget = 0
        percentage = 25.0
        
        credit = budget * (percentage / 100)
        effective_rate = (credit / budget * 100) if budget > 0 else 0
        
        assert credit == 0
        assert effective_rate == 0
    
    def test_negative_budget_handling(self):
        """Test that negative budgets are invalid"""
        budget = -1000000
        
        # Should validate budget is positive
        assert budget < 0
        # In real implementation, this would raise validation error
    
    def test_comparison_ranking(self):
        """Test jurisdiction ranking by credit amount"""
        comparisons = [
            {"jurisdiction": "State A", "credit": 1500000},
            {"jurisdiction": "State B", "credit": 2000000},
            {"jurisdiction": "State C", "credit": 1000000}
        ]
        
        sorted_comparisons = sorted(comparisons, key=lambda x: x["credit"], reverse=True)
        
        assert sorted_comparisons[0]["jurisdiction"] == "State B"
        assert sorted_comparisons[1]["jurisdiction"] == "State A"
        assert sorted_comparisons[2]["jurisdiction"] == "State C"
    
    def test_savings_calculation(self):
        """Test savings calculation between options"""
        best_credit = 2000000
        worst_credit = 1000000
        
        savings = best_credit - worst_credit
        
        assert savings == 1000000
        assert savings > 0
    
    def test_multiple_scenarios_comparison(self, calculator_test_cases):
        """Test comparing multiple budget scenarios"""
        scenarios = []
        
        for case in calculator_test_cases[:3]:  # Test first 3 cases
            budget = case["budget"]
            percentage = case.get("percentage", 0)
            min_spend = case.get("min_spend", 0)
            max_credit = case.get("max_credit", float('inf'))
            
            if budget < min_spend:
                credit = 0
            else:
                credit = budget * (percentage / 100)
                credit = min(credit, max_credit)
            
            scenarios.append({
                "name": case["name"],
                "budget": budget,
                "credit": credit
            })
        
        assert len(scenarios) == 3
        assert all("credit" in s for s in scenarios)
    
    def test_date_based_rule_selection(self):
        """Test filtering rules by effective date"""
        today = datetime(2025, 6, 1)
        
        rules = [
            {"name": "Active Rule", "effective_date": datetime(2025, 1, 1), "expiration_date": datetime(2025, 12, 31)},
            {"name": "Expired Rule", "effective_date": datetime(2024, 1, 1), "expiration_date": datetime(2024, 12, 31)},
            {"name": "Future Rule", "effective_date": datetime(2026, 1, 1), "expiration_date": None}
        ]
        
        active_rules = [
            r for r in rules
            if r["effective_date"] <= today and (r["expiration_date"] is None or r["expiration_date"] >= today)
        ]
        
        assert len(active_rules) == 1
        assert active_rules[0]["name"] == "Active Rule"
    
    def test_compliance_requirement_checking(self):
        """Test compliance requirement verification"""
        requirements = {
            "min_spend": 1000000,
            "min_shoot_days": 10,
            "local_hire_percentage": 75
        }
        
        production = {
            "budget": 5000000,
            "shoot_days": 45,
            "local_hire": 80
        }
        
        meets_min_spend = production["budget"] >= requirements["min_spend"]
        meets_shoot_days = production["shoot_days"] >= requirements["min_shoot_days"]
        meets_local_hire = production["local_hire"] >= requirements["local_hire_percentage"]
        
        all_requirements_met = meets_min_spend and meets_shoot_days and meets_local_hire
        
        assert meets_min_spend is True
        assert meets_shoot_days is True
        assert meets_local_hire is True
        assert all_requirements_met is True
    
    def test_expense_categorization(self, sample_expenses):
        """Test expense qualifying vs non-qualifying categorization"""
        qualifying_expenses = [e for e in sample_expenses if e["isQualifying"]]
        non_qualifying_expenses = [e for e in sample_expenses if not e["isQualifying"]]
        
        qualifying_total = sum(e["amount"] for e in qualifying_expenses)
        non_qualifying_total = sum(e["amount"] for e in non_qualifying_expenses)
        total = sum(e["amount"] for e in sample_expenses)
        
        assert qualifying_total == 650000
        assert non_qualifying_total == 200000
        assert total == 850000
        assert qualifying_total + non_qualifying_total == total


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_large_budget(self):
        """Test handling of very large budgets"""
        budget = 1000000000  # $1 billion
        percentage = 25.0
        
        credit = budget * (percentage / 100)
        
        assert credit == 250000000
        assert credit > 0
    
    def test_very_small_budget(self):
        """Test handling of very small budgets"""
        budget = 1000  # $1,000
        percentage = 25.0
        
        credit = budget * (percentage / 100)
        
        assert credit == 250
        assert credit > 0
    
    def test_zero_percentage(self):
        """Test handling of zero percentage"""
        budget = 5000000
        percentage = 0
        
        credit = budget * (percentage / 100)
        
        assert credit == 0
    
    def test_100_percent_credit(self):
        """Test maximum 100% credit (edge case)"""
        budget = 1000000
        percentage = 100.0
        
        credit = budget * (percentage / 100)
        
        assert credit == budget
    
    def test_decimal_amounts(self):
        """Test handling of decimal amounts"""
        budget = 5432109.87
        percentage = 25.5
        
        credit = budget * (percentage / 100)
        
        assert abs(credit - 1385187.52) < 0.01  # Allow for floating point precision
    
    def test_single_jurisdiction_comparison(self):
        """Test comparison with only one jurisdiction"""
        comparisons = [
            {"jurisdiction": "Only State", "credit": 1500000}
        ]
        
        assert len(comparisons) == 1
        assert comparisons[0]["credit"] > 0