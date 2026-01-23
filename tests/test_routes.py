import requests
from fastapi import FastAPI
import uvicorn

# Test existing endpoints
print("Testing existing endpoints on http://localhost:8000")
print("=" * 60)

# Common endpoints to test
test_endpoints = [
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api",
    "/api/v1",
    "/api/v1/clients",
    "/api/v1/incentives",
    "/clients",
    "/incentives",
    "/expenses",
    "/reports"
]

for endpoint in test_endpoints:
    try:
        response = requests.get(f"http://localhost:8000{endpoint}", timeout=2)
        print(f"{endpoint:30} -> {response.status_code} {response.reason}")
        if response.status_code == 200 and len(response.content) < 100:
            print(f"  Content: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"{endpoint:30} -> Connection refused")
    except requests.exceptions.Timeout:
        print(f"{endpoint:30} -> Timeout")
    except Exception as e:
        print(f"{endpoint:30} -> Error: {e}")

# Try to get the OpenAPI schema
print("\n" + "=" * 60)
print("Checking OpenAPI schema...")
try:
    response = requests.get("http://localhost:8000/openapi.json")
    if response.status_code == 200:
        schema = response.json()
        print(f"✅ OpenAPI schema loaded")
        print(f"   Title: {schema.get('info', {}).get('title', 'Unknown')}")
        print(f"   Version: {schema.get('info', {}).get('version', 'Unknown')}")
        print(f"   Total paths: {len(schema.get('paths', {}))}")
        
        if schema.get('paths'):
            print("\nAvailable paths:")
            for path in sorted(schema.get('paths', {}).keys()):
                print(f"  {path}")
        else:
            print("\n❌ No paths defined in OpenAPI schema")
    else:
        print(f"❌ Could not get OpenAPI schema: {response.status_code}")
except Exception as e:
    print(f"❌ Error getting schema: {e}")