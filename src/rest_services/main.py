from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.rest_services.middleware import MetricsMiddleware

from .routers import payload_router, simple_router, stream_router

app = FastAPI(title="REST Benchmark Service")
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.add_middleware(MetricsMiddleware)

app.include_router(simple_router.router, prefix="/api", tags=["simple"])
app.include_router(stream_router.router, prefix="/api", tags=["stream"])
app.include_router(payload_router.router, prefix="/api", tags=["payload"])
