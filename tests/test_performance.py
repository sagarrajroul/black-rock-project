from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_performance_metrics_success():
    response = client.get("/api/blackrock/challenge/v1/performance")

    assert response.status_code == 200

    data = response.json()

    assert "response_time_ms" in data
    assert "memory_usage_mb" in data
    assert "thread_count" in data

    assert isinstance(data["response_time_ms"], (int, float))
    assert isinstance(data["memory_usage_mb"], (int, float))
    assert isinstance(data["thread_count"], int)


def test_performance_values_are_positive():
    response = client.get("/api/blackrock/challenge/v1/performance")
    data = response.json()

    assert data["response_time_ms"] >= 0
    assert data["memory_usage_mb"] > 0
    assert data["thread_count"] > 0


def test_performance_response_structure():
    response = client.get("/api/blackrock/challenge/v1/performance")
    data = response.json()

    assert set(data.keys()) == {
        "response_time_ms",
        "memory_usage_mb",
        "thread_count"
    }