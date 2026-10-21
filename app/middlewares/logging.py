"""
HTTP request logging middleware.
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


logger = logging.getLogger("app.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs HTTP requests, response status codes, and processing time.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        method = request.method
        path = request.url.path

        request_id = getattr(request.state, "request_id", "-")
        correlation_id = getattr(request.state, "correlation_id", "-")

        start_time = time.perf_counter()

        try:
            response: Response = await call_next(request)

        except Exception:
            duration_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.exception(
                "request_id=%s correlation_id=%s "
                "method=%s path=%s duration_ms=%.2f "
                "outcome=exception",
                request_id,
                correlation_id,
                method,
                path,
                duration_ms,
            )

            raise

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        status_code = response.status_code

        log_method = (
            logger.error
            if status_code >= 500
            else logger.warning
            if status_code >= 400
            else logger.info
        )

        log_method(
            "request_id=%s correlation_id=%s "
            "method=%s path=%s status_code=%s "
            "duration_ms=%.2f",
            request_id,
            correlation_id,
            method,
            path,
            status_code,
            duration_ms,
        )

        return response
    