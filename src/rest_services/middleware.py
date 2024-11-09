import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.rest_services.utils.metrics import REQUEST_COUNT, REQUEST_LATENCY


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/metrics") or request.url.path.startswith(
            "/docs"
        ):
            return await call_next(request)

        start_time = time.perf_counter()
        response: Response = await call_next(request)
        duration = time.perf_counter() - start_time

        method = request.method
        # endpoint = request.url.path
        service = "rest"

        # Determine service type based on the endpoint path
        endpoint = request.url.path
        if endpoint.startswith("/api/simple"):
            service_type = "simple"
        elif endpoint.startswith("/api/stream"):
            service_type = "stream"
        elif endpoint.startswith("/api/payload"):
            service_type = "payload"
        else:
            service_type = "unknown"

        # Record request latency
        REQUEST_LATENCY.labels(
            service=service, method=method, endpoint=service_type
        ).observe(duration)

        # Record request count
        REQUEST_COUNT.labels(
            service=service,
            method=method,
            endpoint=service_type,
            http_status=str(response.status_code),
        ).inc()

        return response
