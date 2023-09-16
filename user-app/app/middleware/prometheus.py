
import time
from typing import Tuple

from prometheus_client import REGISTRY, Counter, Gauge, Histogram, Info
from prometheus_client.openmetrics.exposition import (CONTENT_TYPE_LATEST,
                                                      generate_latest)
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Match
from starlette.types import ASGIApp

INFO = Gauge(
    "fastapi_app_info", "FastAPI application information.", [
        "app_name"]
)

METRICS_REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Application Request Latency", ["method", "path"]
)

METRICS_REQUEST_COUNT = Counter(
    "app_request_count",
    "Application Request Count",
    ["method", "path", "http_status"],
)

METRICS_INFO = Info("app_version", "Application Version")


class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, app_name: str = "fastapi-app") -> None:
        super().__init__(app)
        self.app_name = app_name
        INFO.labels(app_name=self.app_name).inc()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path, is_handled_path = self.get_path(request)

        if not is_handled_path:
            return await call_next(request)

        status_code = None
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            status_code = response.status_code

            end_time = time.perf_counter()

            request_latency = start_time - end_time
            METRICS_REQUEST_LATENCY.labels(request.method, path).observe(
                request_latency
            )
        finally:
            METRICS_REQUEST_COUNT.labels(
                request.method, path, status_code
            ).inc()

        return response

    @staticmethod
    def get_path(request: Request) -> Tuple[str, bool]:
        for route in request.app.routes:
            match, child_scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path, True

        return request.url.path, False


def metrics(request: Request) -> Response:
    return Response(generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST})
