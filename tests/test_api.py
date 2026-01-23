import requests
import json
import time

def test_api_endpoints():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Tax Incentive Compliance Platform API")
    print("=" * 70)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/v1/clients", "Get all clients"),
        ("/api/v1/clients?limit=3", "Get 3 clients"),
        ("/api/v1/incentives", "Get all incentives"),
        ("/api/v1/incentives?status=approved", "Get approved incentives"),
        ("/api/v1/expenses", "Get all expenses"),
        ("/api/v1/reports", "Get all reports"),
        ("/api/v1/stats", "Get platform statistics")
    ]
    
    for endpoint, description in endpoints:
        full_url = f"{base_url}{endpoint}"
        try:
            print(f"\n🔍 Testing: {description}")
            print(f"   URL: {full_url}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ Status: {response.status_code}")
                
                data = response.json()
                
                if isinstance(data, list):
                    print(f"   📊 Items: {len(data)}")
                    if len(data) > 0:
                        # Show first item keys
                        first_item = data[0]
                        if isinstance(first_item, dict):
                            print(f"   📝 First item keys: {list(first_item.keys())[:5]}...")
                elif isinstance(data, dict):
                    if 'message' in data:
                        print(f"   💬 Message: {data['message']}")
                    else:
                        print(f"   📝 Keys: {list(data.keys())}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection refused - Is the server running?")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 Summary:")
    print("• The API should now have working endpoints")
    print("• Visit http://localhost:8000/docs for interactive documentation")
    print("• Test with real data from your database")

if __name__ == "__main__":
    # Wait a moment for server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    test_api_endpoints()