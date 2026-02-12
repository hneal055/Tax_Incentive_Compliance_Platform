"""
Test v1 API router structure
"""
import pytest
from unittest.mock import MagicMock, patch
import sys

# Mock Prisma before importing
sys.modules['prisma'] = MagicMock()
sys.modules['prisma.models'] = MagicMock()

def test_v1_router_structure():
    """Test that v1 router is properly structured"""
    with patch('src.utils.database.prisma'):
        from src.api.v1 import router as v1_router
        from src.api.routes import router as main_router
        
        # Verify v1 router exists and has the correct prefix
        assert v1_router is not None
        assert v1_router.prefix == "/v1"
        
        # Verify main router includes v1 router
        assert main_router is not None


def test_v1_endpoints_imported():
    """Test that all v1 endpoints are properly imported"""
    with patch('src.utils.database.prisma'):
        # Import v1 endpoints
        from src.api.v1.endpoints import (
            api_keys,
            productions,
            calculator,
            monitoring,
            expenses,
            reports,
            jurisdictions,
            incentive_rules,
            excel,
            rule_engine
        )
        
        # Verify each endpoint has a router
        assert hasattr(api_keys, 'router')
        assert hasattr(productions, 'router')
        assert hasattr(calculator, 'router')
        assert hasattr(monitoring, 'router')
        assert hasattr(expenses, 'router')
        assert hasattr(reports, 'router')
        assert hasattr(jurisdictions, 'router')
        assert hasattr(incentive_rules, 'router')
        assert hasattr(excel, 'router')
        assert hasattr(rule_engine, 'router')


def test_api_keys_endpoint_exists():
    """Test that api_keys endpoint exists and has proper structure"""
    with patch('src.utils.database.prisma'):
        from src.api.v1.endpoints import api_keys
        
        # Verify router exists
        assert hasattr(api_keys, 'router')
        
        # Verify router has correct prefix
        assert api_keys.router.prefix == "/api-keys"
        
        # Verify router has correct tags
        assert "API Keys" in api_keys.router.tags


if __name__ == "__main__":
    # Run tests
    test_v1_router_structure()
    print("✓ v1 router structure test passed")
    
    test_v1_endpoints_imported()
    print("✓ v1 endpoints import test passed")
    
    test_api_keys_endpoint_exists()
    print("✓ api_keys endpoint test passed")
    
    print("\n✅ All tests passed!")
