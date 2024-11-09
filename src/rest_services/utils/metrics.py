from prometheus_client import Counter, Histogram, Summary

# Histogram for request latency per endpoint
REQUEST_LATENCY = Histogram(
    "rest_request_latency_seconds",
    "Latency of REST requests in seconds",
    ["service", "method", "endpoint"],
)

# Counter for request counts per endpoint
REQUEST_COUNT = Counter(
    "rest_request_count_total",
    "Total number of REST requests",
    ["service", "method", "endpoint", "http_status"],
)

# Summary for request size per endpoint (if needed for deeper analysis)
REQUEST_SIZE = Summary("rest_request_size_bytes", "Request size in bytes", ["service"])
