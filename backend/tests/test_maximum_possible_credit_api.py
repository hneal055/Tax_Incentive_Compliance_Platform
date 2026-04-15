import pytest
import httpx

from src.main import app
from src.utils.auth_utils import create_access_token


@pytest.mark.asyncio
async def test_new_jersey_maximum_possible_credit_summary():
    transport = httpx.ASGITransport(app=app)
    token = create_access_token({"sub": "test-user", "email": "test@example.com", "role": "admin"})

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/api/0.1.0/maximize/maximum-possible-credit",
            params={"jurisdiction": "New Jersey", "budget": 2500000},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200, response.text
    payload = response.json()

    assert payload.get("best_case_headline") == "Up to 47.0% + sales tax exemption"
    assert "summaries" in payload and len(payload["summaries"]) >= 1

    summary = payload["summaries"][0]
    assert summary["jurisdiction"] == "New Jersey"
    assert summary["maximum_credit_percent"] == 47.0

    benefit_types = [b.get("type") for b in summary.get("additional_benefits", [])]
    assert "sales_tax_exemption" in benefit_types