import pytest
from httpx import AsyncClient
from fastapi import status
from main import app  # Adjust if your app is elsewhere

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_get_incentive_rules_no_filters(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/")
    assert resp.status_code == status.HTTP_200_OK
    assert "items" in resp.json()

@pytest.mark.anyio
async def test_get_incentive_rules_with_jurisdiction(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?jurisdiction_id=test-jurisdiction")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_with_incentive_type(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?incentive_type=grant")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_with_active(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?active=true")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_pagination(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page=2&page_size=10")
    assert resp.status_code == status.HTTP_200_OK

@pytest.mark.anyio
async def test_get_incentive_rules_invalid_page(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page=0")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.anyio
async def test_get_incentive_rules_invalid_page_size(async_client):
    resp = await async_client.get("/api/v1/incentive-rules/?page_size=101")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY