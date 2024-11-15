# **Design Document for Microservices Benchmark: REST vs. gRPC**

## **1. Overview**

This project benchmarks the performance of **REST** and **gRPC** protocols in a microservices architecture. It evaluates the protocols on three types of services: **Simple Request-Response**, **Streaming Data**, and **Large Payload Handling**, with metrics analyzed for **latency**, **throughput**, and **resource utilization**.

The project uses **Prometheus** and **Grafana** for monitoring and visualization, and **Locust** for load testing.

---

## **2. Functional Requirements**

### **2.1 Services**

1. **Simple Service**: Lightweight request-response interactions (e.g., fetching user details).
2. **Streaming Service**: Continuous data streaming (e.g., real-time sensor data).
3. **Large Payload Service**: Handling large data payloads (e.g., file uploads).

### **2.2 Testing**

1. **Unit Testing**: Verifies correctness of service logic.
2. **Load Testing**: Simulates concurrent users for performance analysis.

### **2.3 Monitoring**

- Prometheus: Monitors latency, throughput, and resource metrics.
- Grafana: Provides real-time visualizations and comparative dashboards.

---

## **3. Technologies Used**

| **Technology**    | **Description**                                                            |
| ----------------- | -------------------------------------------------------------------------- |
| **FastAPI**       | High-performance Python framework for REST APIs.                           |
| **gRPC**          | High-performance RPC framework using Protocol Buffers.                     |
| **Prometheus**    | Time-series monitoring system with PromQL for querying metrics.            |
| **Grafana**       | Visualization tool for creating real-time dashboards from Prometheus data. |
| **Node Exporter** | Prometheus exporter for hardware and OS-level metrics.                     |
| **Locust**        | Python-based load testing framework, simulating millions of users.         |

---

## **4. Architecture and Design**

### **4.1 High-Level Architecture**

Below is the **high-level architecture** of the microservices benchmark system:

```plaintext
+------------------+        +------------------+        +------------------+
| REST Service     |        | gRPC Service     |        | Node Exporter     |
| /metrics         |        | /metrics         |        | /metrics          |
+------------------+        +------------------+        +------------------+
         |                           |                           |
         |                           |                           |
         +-----------+---------------+---------------------------+
                     |
            +--------------------+
            | Prometheus Server  |
            | (Scrapes Metrics)  |
            +--------------------+
                     |
            +--------------------+
            | Grafana Dashboards |
            | (Visualizes Data)  |
            +--------------------+
```

---

### **4.2 Deployment Diagram**

```plaintext
+-----------------------------+       +-----------------------------+
|       REST Service          |       |        gRPC Service         |
| Dockerized Microservices    |       | Dockerized Microservices    |
| Port: 8001                 +--------+ Port: 8002                 |
+-----------------------------+       +-----------------------------+
              |                                   |
              |                                   |
       +-------------+                     +-------------+
       | Prometheus  |                     | Grafana     |
       | Collects    |                     | Dashboards  |
       | Metrics     |                     | Port: 3000  |
       +-------------+                     +-------------+
```

---

## **5. Prometheus Queries**

### **5.1 Latency**

1. **REST Simple Service (P50):**
   ```promql
   histogram_quantile(0.5, sum(rate(rest_request_latency_seconds_bucket{service="rest", endpoint="simple"}[1m])) by (le))
   ```
2. **gRPC Simple Service (P50):**
   ```promql
   histogram_quantile(0.5, sum(rate(grpc_request_latency_seconds_bucket{service="benchmark.SimpleService"}[1m])) by (le))
   ```

### **5.2 Throughput**

1. **REST Simple Service:**
   ```promql
   sum(rate(rest_request_count_total{service="rest", endpoint="simple"}[1m]))
   ```
2. **gRPC Simple Service:**
   ```promql
   sum(rate(grpc_request_count_total{service="benchmark.SimpleService"}[1m]))
   ```

### **5.3 Resource Utilization**

1. **CPU Utilization**:
   ```promql
   sum(rate(node_cpu_seconds_total{mode!="idle"}[1m])) / sum(rate(node_cpu_seconds_total[1m])) * 100
   ```
2. **Memory Usage**:
   ```promql
   node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
   ```
3. **Network Usage**:
   ```promql
   rate(node_network_receive_bytes_total[1m])
   ```

---

## **6. Example Test Scripts**

### **6.1 Unit Test Example (REST Simple Service)**

```python
import unittest
from fastapi.testclient import TestClient
from src.rest_services.main import app

class TestSimpleService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_simple_data(self):
        response = self.client.get("/api/simple")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
```

### **6.2 Load Test Example (REST Simple Service)**

```python
from locust import HttpUser, task

class SimpleServiceUser(HttpUser):
    @task
    def get_simple_data(self):
        self.client.get("/api/simple")
```

### **6.3 Load Test Example (gRPC Streaming Service)**

```python
import grpc
from locust import User, task, between
from proto.service_definitions_pb2_grpc import SimpleServiceStub
from proto.service_definitions_pb2 import StreamRequest

class GRPCUser(User):
    wait_time = between(1, 5)

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:8002")
        self.stub = SimpleServiceStub(self.channel)

    @task
    def stream_data(self):
        request = StreamRequest(data="test_data")
        for response in self.stub.StreamData(request):
            pass
```

---

## **7. Monitoring and Visualization**

### **7.1 Prometheus Configuration**

Prometheus scrapes metrics from the following targets:

- REST Service: `http://rest-service:8001/metrics`
- gRPC Service: `http://grpc-service:8002/metrics`
- Node Exporter: `http://node-exporter:9100/metrics`

---

### **7.2 Grafana Dashboards**

**Sample Panels**:

1. **REST Latency (P50, P95)**:
   ```promql
   histogram_quantile(0.5, sum(rate(rest_request_latency_seconds_bucket{endpoint="simple"}[1m])) by (le))
   histogram_quantile(0.95, sum(rate(rest_request_latency_seconds_bucket{endpoint="simple"}[1m])) by (le))
   ```
2. **REST Throughput**:
   ```promql
   sum(rate(rest_request_count_total{endpoint="simple"}[1m]))
   ```
3. **CPU Utilization**:
   ```promql
   sum(rate(node_cpu_seconds_total{mode!="idle"}[1m])) / sum(rate(node_cpu_seconds_total[1m])) * 100
   ```
4. **Memory Utilization**:
   ```promql
   100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)
   ```

---

## **8. Results**

### **8.1 Metrics Comparison**

| **Metric**      | **REST** | **gRPC** |
| --------------- | -------- | -------- |
| Latency (P50)   | 15 ms    | 5 ms     |
| Throughput      | 300 ms   | 500 ms   |
| CPU Utilization | 30%      | 25%      |
| Memory Usage    | 100 MB   | 75 MB    |
