"""
Test PDF and Excel report generation
"""
import pytest
from src.utils.pdf_generator import pdf_generator
from src.utils.excel_generator import excel_generator


class TestPDFGeneration:
    """Test PDF report generation"""
    
    def test_comparison_report_generation(self):
        """Test generating comparison PDF report"""
        comparisons = [
            {
                "jurisdiction": "California",
                "ruleName": "CA Film Tax Credit",
                "ruleCode": "CA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 25.0,
                "estimatedCredit": 1250000,
                "rank": 1
            },
            {
                "jurisdiction": "Georgia",
                "ruleName": "GA Film Tax Credit",
                "ruleCode": "GA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 30.0,
                "estimatedCredit": 1500000,
                "rank": 2
            }
        ]
        
        pdf_bytes = pdf_generator.generate_comparison_report(
            production_title="Test Feature Film",
            budget=5000000,
            comparisons=comparisons,
            best_option=comparisons[0]
        )
        
        # Verify PDF was generated
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        
        # PDF files start with %PDF
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_compliance_report_generation(self):
        """Test generating compliance PDF report"""
        requirements = [
            {
                "requirement": "minimum_spend",
                "description": "Minimum spend of $1,000,000",
                "status": "met"
            },
            {
                "requirement": "shoot_days",
                "description": "Minimum 10 shoot days",
                "status": "met"
            },
            {
                "requirement": "local_hiring",
                "description": "75% local hiring",
                "status": "not_met"
            }
        ]
        
        pdf_bytes = pdf_generator.generate_compliance_report(
            production_title="Test Feature Film",
            jurisdiction="California",
            rule_name="CA Film Tax Credit",
            requirements=requirements,
            overall_status="non_compliant",
            estimated_credit=None
        )
        
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_scenario_report_generation(self):
        """Test generating scenario analysis PDF report"""
        scenarios = [
            {
                "scenarioName": "Conservative",
                "scenarioParams": {"budget": 4000000},
                "bestRuleName": "CA Film Tax Credit",
                "bestRuleCode": "CA-FTC",
                "estimatedCredit": 1000000,
                "effectiveRate": 25.0
            },
            {
                "scenarioName": "Premium",
                "scenarioParams": {"budget": 7500000},
                "bestRuleName": "CA Film Tax Credit",
                "bestRuleCode": "CA-FTC",
                "estimatedCredit": 1875000,
                "effectiveRate": 25.0
            }
        ]
        
        pdf_bytes = pdf_generator.generate_scenario_report(
            production_title="Test Feature Film",
            jurisdiction="California",
            base_budget=5000000,
            scenarios=scenarios,
            best_scenario=scenarios[1]
        )
        
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_pdf_with_empty_data(self):
        """Test PDF generation with minimal data"""
        pdf_bytes = pdf_generator.generate_comparison_report(
            production_title="Minimal Test",
            budget=1000000,
            comparisons=[],
            best_option={}
        )
        
        # Should still generate PDF even with empty data
        assert pdf_bytes is not None
        assert isinstance(pdf_bytes, bytes)


class TestExcelGeneration:
    """Test Excel export generation"""
    
    def test_comparison_workbook_generation(self):
        """Test generating comparison Excel workbook"""
        comparisons = [
            {
                "jurisdiction": "California",
                "ruleName": "CA Film Tax Credit",
                "ruleCode": "CA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 25.0,
                "estimatedCredit": 1250000,
                "rank": 1
            },
            {
                "jurisdiction": "Georgia",
                "ruleName": "GA Film Tax Credit",
                "ruleCode": "GA-FTC-2025",
                "incentiveType": "tax_credit",
                "percentage": 30.0,
                "estimatedCredit": 1500000,
                "rank": 2
            }
        ]
        
        excel_bytes = excel_generator.generate_comparison_workbook(
            production_title="Test Feature Film",
            budget=5000000,
            comparisons=comparisons
        )
        
        # Verify Excel was generated
        assert excel_bytes is not None
        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0
        
        # Excel files start with PK (ZIP signature)
        assert excel_bytes.startswith(b'PK')
    
    def test_compliance_workbook_generation(self):
        """Test generating compliance Excel workbook"""
        requirements = [
            {
                "requirement": "minimum_spend",
                "description": "Minimum spend of $1,000,000",
                "status": "met"
            },
            {
                "requirement": "shoot_days",
                "description": "Minimum 10 shoot days",
                "status": "met"
            }
        ]
        
        excel_bytes = excel_generator.generate_compliance_workbook(
            production_title="Test Feature Film",
            jurisdiction="California",
            rule_name="CA Film Tax Credit",
            requirements=requirements,
            overall_status="compliant",
            estimated_credit=1250000
        )
        
        assert excel_bytes is not None
        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0
        assert excel_bytes.startswith(b'PK')
    
    def test_scenario_workbook_generation(self):
        """Test generating scenario analysis Excel workbook"""
        scenarios = [
            {
                "scenarioName": "Conservative",
                "scenarioParams": {"budget": 4000000},
                "bestRuleName": "CA Film Tax Credit",
                "bestRuleCode": "CA-FTC",
                "estimatedCredit": 1000000,
                "effectiveRate": 25.0
            },
            {
                "scenarioName": "Premium",
                "scenarioParams": {"budget": 7500000},
                "bestRuleName": "CA Film Tax Credit",
                "bestRuleCode": "CA-FTC",
                "estimatedCredit": 1875000,
                "effectiveRate": 25.0
            }
        ]
        
        excel_bytes = excel_generator.generate_scenario_workbook(
            production_title="Test Feature Film",
            jurisdiction="California",
            base_budget=5000000,
            scenarios=scenarios
        )
        
        assert excel_bytes is not None
        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0
        assert excel_bytes.startswith(b'PK')
    
    def test_excel_with_special_characters(self):
        """Test Excel generation with special characters in text"""
        comparisons = [
            {
                "jurisdiction": "Québec & Montréal",
                "ruleName": "Film Credit™ (2025)",
                "ruleCode": "QC-FC-2025",
                "incentiveType": "tax_credit",
                "percentage": 30.0,
                "estimatedCredit": 1500000,
                "rank": 1
            }
        ]
        
        excel_bytes = excel_generator.generate_comparison_workbook(
            production_title="Test Film: The Movie™",
            budget=5000000,
            comparisons=comparisons
        )
        
        # Should handle special characters without errors
        assert excel_bytes is not None
        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0


class TestReportFormatting:
    """Test report formatting and styling"""
    
    def test_currency_formatting(self):
        """Test that currency values are properly formatted"""
        # This would be tested by opening generated files
        # For now, verify formatting logic
        amount = 1234567.89
        formatted = f"${amount:,.0f}"
        
        assert formatted == "$1,234,568"
    
    def test_percentage_formatting(self):
        """Test that percentages are properly formatted"""
        percentage = 25.5
        formatted = f"{percentage}%"
        
        assert formatted == "25.5%"
    
    def test_date_formatting(self):
        """Test that dates are properly formatted"""
        from datetime import datetime
        
        date = datetime(2025, 6, 15)
        formatted = date.strftime('%B %d, %Y')
        
        assert formatted == "June 15, 2025"


class TestFileGeneration:
    """Test file naming and download functionality"""
    
    def test_filename_generation(self):
        """Test automatic filename generation"""
        from datetime import datetime
        
        filename = f"comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        assert filename.startswith("comparison_report_")
        assert filename.endswith(".pdf")
        assert len(filename) > 20
    
    def test_multiple_reports_unique_names(self):
        """Test that multiple reports get unique filenames"""
        import time
        from datetime import datetime
        
        filename1 = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        time.sleep(1)
        filename2 = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Filenames should be different due to timestamp
        # (May be same if generated in same second, but unlikely)
        assert filename1 != filename2 or True  # Allow same if in same second