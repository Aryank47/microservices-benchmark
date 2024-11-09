from locust import HttpUser, between, task


class RESTUser(HttpUser):
    host = "http://localhost:8001"
    wait_time = between(0.1, 1.0)

    @task(3)
    def test_simple_request(self):
        payload = {"message": "test", "data": {"key": "value" * 100}}  # 1KB
        self.client.post("/api/simple", json=payload)

    @task(2)
    def test_stream_data(self):
        self.client.get("/api/stream?messages=100")

    @task(1)
    def test_large_payload(self):
        payload = {"data": "x" * (1024 * 1024), "size_kb": 1024}  # 1MB payload
        self.client.post("/api/payload", json=payload)
