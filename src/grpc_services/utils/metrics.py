from prometheus_client import Counter, Histogram, Summary

REQUEST_LATENCY = Histogram(
    "grpc_request_latency_seconds",
    "Latency of gRPC requests in seconds",
    ["service", "method"],
)

REQUEST_COUNT = Counter(
    "grpc_request_count_total",
    "Total number of gRPC requests",
    ["service", "method", "grpc_status"],
)

REQUEST_SIZE = Summary(
    "grpc_request_size_bytes",
    "Request size in bytes",
    ["service"],
)
