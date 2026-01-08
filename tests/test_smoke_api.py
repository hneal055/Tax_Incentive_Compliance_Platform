import pytest
import httpx

from src.main import app


def _pick_rule_engine_path() -> str:
    """
    Detect the rule-engine evaluate route no matter what version prefix is used.
    Examples:
      /api/v1/rule-engine/evaluate
      /api/0.1.0/rule-engine/evaluate
      /rule-engine/evaluate
    """
    routes = {getattr(r, "path", "") for r in app.router.routes}

    candidates = sorted(
        p for p in routes
        if p.startswith("/api/") and p.endswith("/rule-engine/evaluate")
    )
    if candidates:
        return candidates[0]

    if "/rule-engine/evaluate" in routes:
        return "/rule-engine/evaluate"

    raise AssertionError(
        "Rule engine evaluate route not found. Available routes:\n"
        + "\n".join(sorted(p for p in routes if p))
    )


@pytest.mark.anyio
async def test_api_smoke_rule_engine_evaluate_200():
    path = _pick_rule_engine_path()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "jurisdiction_code": "IL",
            "expenses": [{"category": "production", "amount": "1000.00"}],
        }
        r = await client.post(path, json=payload)
        assert r.status_code == 200, f"path={path} status={r.status_code} body={r.text}"

        data = r.json()
        assert "jurisdiction_code" in data
        assert "total_eligible_spend" in data
        assert "total_incentive_amount" in data
        assert isinstance(data.get("breakdown"), list)


@pytest.mark.anyio
async def test_api_smoke_unknown_jurisdiction_404():
    path = _pick_rule_engine_path()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"jurisdiction_code": "ZZ", "expenses": []}
        r = await client.post(path, json=payload)
        assert r.status_code == 404, f"path={path} status={r.status_code} body={r.text}"
