Set-Location C:\Projects\Tax_Incentive_Compliance_Platform; @'
import os
import socket
import subprocess
import sys
import time

import pytest


def _is_port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _wait_for_health(base: str, timeout_s: float = 20.0) -> bool:
    try:
        import requests
    except Exception:
        return False

    url = base.rstrip("/") + "/health"
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def _start_uvicorn(host: str, port: int) -> subprocess.Popen:
    cmd = [
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--host", host,
        "--port", str(port),
        "--log-level", "warning",
    ]

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]

    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creationflags,
    )


def _stop_process(p: subprocess.Popen) -> None:
    if p.poll() is not None:
        return
    try:
        p.terminate()
        p.wait(timeout=5)
    except Exception:
        try:
            p.kill()
        except Exception:
            pass


def test_api_smoke_rule_engine_evaluate_200():
    """
    Integration smoke test that can self-start the API.

    Env:
      - API_BASE_URL (default http://127.0.0.1:8000)
      - SKIP_API_SMOKE=1 to skip
      - AUTO_START_API=0 to disable self-start (default enabled)
      - API_HOST / API_PORT override host/port for auto-start
    """
    if os.getenv("SKIP_API_SMOKE", "").strip() == "1":
        pytest.skip("SKIP_API_SMOKE=1")

    try:
        import requests
    except Exception:
        pytest.skip("requests not installed")

    base = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    auto_start = os.getenv("AUTO_START_API", "1").strip() != "0"

    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))

    proc = None
    try:
        if auto_start and ("127.0.0.1" in base or "localhost" in base):
            if not _is_port_open(host, port):
                proc = _start_uvicorn(host, port)

        assert _wait_for_health(base, timeout_s=25.0), f"API not healthy at {base}/health"

        url = f"{base}/api/v1/rule-engine/evaluate"
        payload = {
            "jurisdiction_code": "IL",
            "expenses": [
                {"category": "production", "amount": "1000.00"},
                {"category": "payroll", "amount": "500.00", "is_payroll": True},
                {"category": "travel", "amount": "250.00"},
            ],
        }

        r = requests.post(url, json=payload, timeout=10)
        assert r.status_code == 200, r.text
        data = r.json()

        # Contract stability
        assert "jurisdiction_code" in data
        assert "total_eligible_spend" in data
        assert "total_incentive_amount" in data
        assert "breakdown" in data

        assert data["jurisdiction_code"] == "IL"
        assert float(data["total_eligible_spend"]) == pytest.approx(1500.0)
        assert float(data["total_incentive_amount"]) == pytest.approx(450.0)
        assert isinstance(data["breakdown"], list)

    finally:
        if proc is not None:
            _stop_process(proc)
'@ | Out-File -FilePath .\tests\test_smoke_api.py -Encoding utf8
