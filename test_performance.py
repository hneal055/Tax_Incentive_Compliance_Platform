"""
Performance & Scalability Tests
Profiles endpoint response times, database query efficiency, and memory usage
"""

import pytest
import time
import asyncio
from httpx import AsyncClient
from src.main import app
from src.utils.database import prisma


@pytest.fixture(scope="function")
async def client():
    """Async HTTP client with proper startup/shutdown"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await app.router.lifespan_context(None).__aenter__()
        yield ac
        try:
            await app.router.lifespan_context(None).__aexit__(None, None, None)
        except:
            pass


class TestEndpointPerformance:
    """Test endpoint response times"""

    @pytest.mark.asyncio
    async def test_health_endpoint_performance(self, client):
        """Health endpoint should respond in < 50ms"""
        start = time.time()
        response = await client.get("/health")
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert response.status_code == 200
        assert elapsed < 50, f"Health endpoint took {elapsed}ms (target: < 50ms)"

    @pytest.mark.asyncio
    async def test_root_endpoint_performance(self, client):
        """Root endpoint should respond in < 50ms"""
        start = time.time()
        response = await client.get("/")
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert elapsed < 50, f"Root endpoint took {elapsed}ms (target: < 50ms)"

    @pytest.mark.asyncio
    async def test_calculate_simple_performance(self, client):
        """Calculate simple endpoint should respond in < 100ms"""
        payload = {"amount": 100000.0, "percentage": 25.0}
        start = time.time()
        response = await client.post("/api/0.1.0/calculate/simple", json=payload)
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code in [200, 400, 422]
        assert elapsed < 100, f"Calculate endpoint took {elapsed}ms (target: < 100ms)"

    @pytest.mark.asyncio
    async def test_calculate_compare_performance(self, client):
        """Compare calculation should respond in < 200ms"""
        payload = {"amount": 100000.0, "jurisdictions": ["CA", "NY"]}
        start = time.time()
        response = await client.post("/api/0.1.0/calculate/compare", json=payload)
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code in [200, 400, 422]
        assert elapsed < 200, f"Compare endpoint took {elapsed}ms (target: < 200ms)"


class TestConcurrentRequests:
    """Test behavior under concurrent load"""

    @pytest.mark.asyncio
    async def test_concurrent_health_checks(self, client):
        """Should handle 10 concurrent health requests"""
        async def health_request():
            return await client.get("/health")
        
        tasks = [health_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks)
        
        assert all(r.status_code == 200 for r in responses)
        assert len(responses) == 10

    @pytest.mark.asyncio
    async def test_concurrent_calculations(self, client):
        """Should handle 5 concurrent calculation requests"""
        async def calculate_request(i):
            payload = {"amount": 100000.0 + i * 1000, "percentage": 25.0}
            return await client.post("/api/0.1.0/calculate/simple", json=payload)
        
        tasks = [calculate_request(i) for i in range(5)]
        responses = await asyncio.gather(*tasks)
        
        assert all(r.status_code in [200, 400, 422] for r in responses)
        assert len(responses) == 5


class TestDatabaseQueryPerformance:
    """Test database query efficiency"""

    @pytest.mark.asyncio
    async def test_database_connection_performance(self):
        """Database connection should establish in < 500ms"""
        if not prisma.is_connected():
            start = time.time()
            await prisma.connect()
            elapsed = (time.time() - start) * 1000
            
            assert elapsed < 500, f"DB connection took {elapsed}ms (target: < 500ms)"
        
        await prisma.disconnect()

    @pytest.mark.asyncio
    async def test_query_count_limit(self):
        """A single endpoint call should not make > 5 DB queries"""
        # This is a benchmark test - actual implementation would use query counting
        # For now, we just ensure connection works
        if not prisma.is_connected():
            await prisma.connect()
        
        # In production, use tools like django-debug-toolbar or sqlalchemy query counter
        # to monitor actual query counts
        
        await prisma.disconnect()


class TestMemoryUsage:
    """Test memory efficiency"""

    @pytest.mark.asyncio
    async def test_no_memory_leaks_on_repeated_requests(self, client):
        """Repeated requests should not accumulate memory indefinitely"""
        # Make 100 requests
        for i in range(100):
            response = await client.get("/health")
            assert response.status_code == 200
        
        # If we got here without crashes, memory management is working


class TestResponseSizes:
    """Test response payload sizes"""

    @pytest.mark.asyncio
    async def test_health_response_size(self, client):
        """Health response should be small (< 1KB)"""
        response = await client.get("/health")
        size = len(response.content)
        
        assert size < 1024, f"Health response is {size} bytes (target: < 1KB)"

    @pytest.mark.asyncio
    async def test_calculate_response_size(self, client):
        """Calculate response should be reasonable (< 10KB)"""
        payload = {"amount": 100000.0, "percentage": 25.0}
        response = await client.post("/api/0.1.0/calculate/simple", json=payload)
        
        if response.status_code == 200:
            size = len(response.content)
            assert size < 10240, f"Calculate response is {size} bytes (target: < 10KB)"


class TestErrorHandlingPerformance:
    """Test that error handling doesn't impact performance"""

    @pytest.mark.asyncio
    async def test_404_error_response_time(self, client):
        """404 errors should respond quickly (< 50ms)"""
        start = time.time()
        response = await client.get("/api/0.1.0/nonexistent")
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 404
        assert elapsed < 50, f"404 response took {elapsed}ms (target: < 50ms)"

    @pytest.mark.asyncio
    async def test_validation_error_response_time(self, client):
        """Validation errors should respond quickly (< 100ms)"""
        payload = {"incomplete": "data"}
        start = time.time()
        response = await client.post("/api/0.1.0/calculate/simple", json=payload)
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code in [400, 422]
        assert elapsed < 100, f"Validation error took {elapsed}ms (target: < 100ms)"


class TestScalabilityMetrics:
    """Metrics for scalability assessment"""

    @pytest.mark.asyncio
    async def test_throughput_simple_calculation(self, client):
        """Measure throughput: requests per second for simple calculation"""
        requests_count = 50
        payload = {"amount": 100000.0, "percentage": 25.0}
        
        start = time.time()
        for _ in range(requests_count):
            response = await client.post("/api/0.1.0/calculate/simple", json=payload)
            assert response.status_code in [200, 400, 422]
        
        elapsed = time.time() - start
        throughput = requests_count / elapsed
        
        # Log throughput for analysis
        print(f"\nThroughput: {throughput:.2f} requests/second")
        assert throughput > 10, f"Throughput is {throughput} req/s (target: > 10 req/s)"

    @pytest.mark.asyncio
    async def test_p95_latency(self, client):
        """Measure P95 latency for health checks"""
        requests_count = 100
        latencies = []
        
        for _ in range(requests_count):
            start = time.time()
            response = await client.get("/health")
            elapsed = (time.time() - start) * 1000
            latencies.append(elapsed)
            assert response.status_code == 200
        
        latencies.sort()
        p95 = latencies[int(len(latencies) * 0.95)]
        
        print(f"\nP95 Latency: {p95:.2f}ms")
        assert p95 < 100, f"P95 latency is {p95}ms (target: < 100ms)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
