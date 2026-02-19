"""
Test Expenses Endpoint
"""
import pytest


@pytest.mark.asyncio
async def test_expenses_endpoint_exists(client):
    """Test that expenses endpoint is accessible"""
    response = await client.get('/api/0.1.0/expenses/')
    
    print(f"\n{'='*70}")
    print(f"Testing:  GET /api/0.1.0/expenses/")
    print(f"Status Code: {response.status_code}")
    print(f"{'='*70}")
    
    # Should return 200 with data structure
    assert response.status_code == 200
    
    data = response.json()
    print(f"✅ Response structure:")
    print(f"   - total: {data.get('total')}")
    print(f"   - totalAmount: {data.get('totalAmount')}")
    print(f"   - qualifyingAmount: {data.get('qualifyingAmount')}")
    print(f"   - expenses: {len(data.get('expenses', []))} items")
    
    # Verify response structure
    assert 'total' in data
    assert 'expenses' in data
    assert 'totalAmount' in data
    assert 'qualifyingAmount' in data
    assert 'nonQualifyingAmount' in data
    assert isinstance(data['expenses'], list)
