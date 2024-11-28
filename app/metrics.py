from prometheus_client import Counter, Histogram, Gauge
import time
from typing import Callable
from starlette.types import ASGIApp, Receive, Scope, Send

# Request metrics
REQUEST_COUNT = Counter(
    'toxicity_api_requests_total',
    'Total requests processed',
    ['endpoint']
)

REQUEST_LATENCY = Histogram(
    'toxicity_api_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf'))
)

# Business metrics
TEXTS_PROCESSED = Counter(
    'toxicity_api_texts_processed_total',
    'Total number of texts processed'
)

BATCH_SIZE = Histogram(
    'toxicity_api_batch_size',
    'Batch sizes of requests',
    buckets=(1, 10, 32, 64, 128, float('inf'))
)

# System metrics
WORKER_COUNT = Gauge(
    'toxicity_api_workers',
    'Number of active workers'
)

ERROR_COUNT = Counter(
    'toxicity_api_errors_total',
    'Total number of errors',
    ['error_type']
)

class MetricsMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        start_time = time.time()

        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                REQUEST_COUNT.labels(endpoint=path).inc()
                REQUEST_LATENCY.labels(endpoint=path).observe(time.time() - start_time)
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        except Exception as e:
            ERROR_COUNT.labels(error_type=type(e).__name__).inc()
            raise