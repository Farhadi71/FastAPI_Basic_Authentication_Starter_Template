"""
Correlation ID middleware.
"""

import re
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


CORRELATION_ID_PATTERN = re.compile(r"^[a-zA-Z0-9._:-]{1,100}$")


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Assigns a correlation ID to each request and returns it in the response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        incoming_id = request.headers.get("X-Correlation-ID", "")

        if CORRELATION_ID_PATTERN.fullmatch(incoming_id):
            correlation_id = incoming_id
        else:
            correlation_id = str(uuid4())

        request.state.correlation_id = correlation_id

        response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id

        return response