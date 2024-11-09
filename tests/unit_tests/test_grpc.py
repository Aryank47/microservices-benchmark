from fastapi.testclient import TestClient

from src.rest_services.main import app

client = TestClient(app)


def test_simple_request():
    response = client.post(
        "/api/simple", json={"message": "hello", "data": {"key": "value"}}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "data": {"key": "value"}}


def test_stream_data():
    response = client.get("/api/stream?messages=10")
    assert response.status_code == 200
    # Validate the stream contains expected content type
    assert response.headers["content-type"] == "application/x-ndjson"


def test_large_payload():
    payload = {"data": "x" * (1024 * 512), "size_kb": 512}  # 512KB payload
    response = client.post("/api/payload", json=payload)
    assert response.status_code == 200
    assert response.json() == {"success": True, "processed_size_kb": 512}
