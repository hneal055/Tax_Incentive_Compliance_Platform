"""
Complete Expenses Endpoint Test
"""
import asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.utils.database import prisma


async def test_expenses_crud():
    """Test all expenses endpoints"""
    
    if not prisma.is_connected():
        await prisma.connect()
        print("✅ Database connected\n")
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        
        print("="*70)
        print("🧪 Testing Expenses Endpoints")
        print("="*70)
        
        # Test 1: List all expenses
        print("\n1. GET /api/0.1.0/expenses/ (List all)")
        response = await client.get('/api/0.1.0/expenses/')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data.get('total', 0)} expenses")
            print(f"   💰 Total Amount: \")
            print(f"   ✓ Qualifying:  \")
            print(f"   ✗ Non-Qualifying: \")
        
        # Test 2: Filter by qualifying status
        print("\n2. GET /api/0.1.0/expenses/?is_qualifying=true")
        response = await client.get('/api/0.1.0/expenses/? is_qualifying=true')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response. json()
            print(f"   ✅ Found {data.get('total', 0)} qualifying expenses")
        
        # Test 3: Filter by category
        print("\n3. GET /api/0.1.0/expenses/?category=labor")
        response = await client.get('/api/0.1.0/expenses/?category=labor')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response. json()
            print(f"   ✅ Found {data.get('total', 0)} labor expenses")
        
        # Test 4: Try to create (will likely fail without valid production ID)
        print("\n4. POST /api/0.1.0/expenses/ (Create)")
        test_expense = {
            'productionId': 'test-id',
            'category': 'labor',
            'description': 'Test expense',
            'amount': 10000.0,
            'isQualifying': True,
            'expenseDate':  '2026-01-22'
        }
        response = await client.post('/api/0.1.0/expenses/', json=test_expense)
        print(f"   Status: {response. status_code}")
        if response.status_code == 201:
            print(f"   ✅ Expense created!")
        elif response.status_code == 404:
            print(f"   ⚠️  Production not found (expected)")
        else:
            print(f"   Response: {response.json()}")
        
        print("\n" + "="*70)
        print("✅ Expenses endpoint testing complete!")
        print("="*70)
    
    if prisma.is_connected():
        await prisma.disconnect()
        print("\n✅ Database disconnected")


if __name__ == '__main__':
    asyncio. run(test_expenses_crud())
