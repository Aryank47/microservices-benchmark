# Microservices Benchmark: REST vs. gRPC

This project benchmarks the performance of REST and gRPC protocols in microservices architectures. It includes services for **Simple Request-Response**, **Streaming Data**, and **Large Payload Handling**, enabling performance comparison through metrics like **latency**, **throughput**, and **resource utilization**.

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Running the Services Locally](#running-the-services-locally)
5. [Monitoring with Prometheus and Grafana](#monitoring-with-prometheus-and-grafana)
6. [Load Testing](#load-testing)
7. [Results](#results)

---

## Overview

This project includes implementations for:

- **Simple Service**: Handles lightweight request-response interactions.
- **Streaming Service**: Supports continuous data streams.
- **Large Payload Service**: Processes large data payloads.

Each service provides:

- **Endpoints** for interaction.
- **Prometheus Metrics** for performance monitoring.

---

## Project Structure

```
microservices-benchmark/
├── proto/
│   └── service_definitions.proto
├── src/
│   ├── rest_services/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── simple_router.py
│   │   │   ├── stream_router.py
│   │   │   └── payload_router.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── metrics.py
│   ├── grpc_services/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── simple_service.py
│   │   │   ├── stream_service.py
│   │   │   └── payload_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── metrics.py
├── tests/
│   ├── __init__.py
│   ├── load_tests/
│   │   ├── __init__.py
│   │   ├── rest_tests.py
│   │   └── grpc_tests.py
│   └── unit_tests/
│       ├── __init__.py
│       ├── test_rest.py
│       └── test_grpc.py
└── deployment/
    ├── docker/
        ├── Dockerfile.rest
        └── Dockerfile.grpc
```

---

## Setup Instructions

### Prerequisites

1. Install **Python 3.11+**.
2. Install **Docker** and **Docker Compose**.

### Clone the Repository

Clone the repository and navigate into the directory:

```bash
git clone https://github.com/Aryank47/microservices-benchmark.git
cd microservices-benchmark
```

### Install Python Dependencies

Use Poetry to install dependencies:

```bash
poetry install
```

---

## Running the Services Locally

### Start All Services

Run the REST and gRPC services using Docker Compose for the local environment:

```bash
docker-compose --build
```

### Access Services

- **REST Metrics**: `http://localhost:8001/metrics`
- **gRPC Metrics**: `http://localhost:8002/metrics`
- **resource utilization Metrics**: `http://localhost:9100/metrics`

---

## Monitoring with Prometheus and Grafana

### Prometheus Setup

Prometheus is preconfigured in `prometheus.yml` to scrape metrics from the REST and gRPC services.

Prometheus will be accessible at: `http://prometheus:9090`.

---

### Grafana Setup

Grafana is used to visualize metrics collected by Prometheus.

Access Grafana at: `http://localhost:3000`.

#### Configure Grafana

1. **Log in**:
   - Default username: `admin`
   - Default password: `admin`
2. **Add Prometheus as a Data Source**:
   - Go to **Configuration > Data Sources > Add Data Source**.
   - Select **Prometheus**.
   - Set the URL to `http://prometheus:9090`.
   - Click **Save & Test**.

#### Create Dashboards

Add dashboards for monitoring latency, throughput, and resource utilization.

##### Example Queries for Metrics

1. **Latency (50th Percentile)**

   - **REST Simple Service**:
     ```prometheus
     histogram_quantile(0.5, sum(rate(rest_request_latency_seconds_bucket{service="rest", endpoint="simple"}[1m])) by (le))
     ```
   - **gRPC Simple Service**:
     `prometheus
histogram_quantile(0.5, sum(rate(grpc_request_latency_seconds_bucket{service="benchmark.SimpleService"}[1m])) by (le))
`
     Similar panels can be setup for other services

2. **Throughput**

   - **REST Simple Service**:
     ```prometheus
     sum(rate(rest_request_count_total{service="rest", endpoint="simple"}[1m]))
     ```
   - **gRPC Simple Service**:
     `prometheus
sum(rate(grpc_request_count_total{service="benchmark.SimpleService"}[1m]))
`
     Similar panels can be setup for other services

3. **CPU Utilization**

   ```prometheus
   sum(rate(node_cpu_seconds_total{job="node-exporter", mode!="idle"}[1m])) / sum(rate(node_cpu_seconds_total{job="node-exporter"}[1m])) * 100
   ```

4. **Memory Usage**
   ```prometheus
   node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
   ```
5. **Network Usage**
   ```prometheus
   rate(node_network_receive_bytes_total[1m])
   ```

---

## Load Testing

### Locust

Use Locust for load testing. Scripts are available in the `tests/load_tests/` directory.

#### Install Locust

Install Locust globally:

```bash
pip install locust
```

#### Run Locust Tests

Run a test targeting the REST service:

```bash
locust -f tests/load_tests/rest_tests.py --headless -u 100 -r 10 --run-time 10m
```

Run a test targeting the gRPC service:

```bash
locust -f tests/load_tests/grpc_tests.py --headless -u 100 -r 10 --run-time 10m
```

---

## Results

- Visualize metrics in Grafana dashboards.
- Export results as CSV from Grafana for further analysis.
- Compare latency and throughput metrics for REST and gRPC services.
