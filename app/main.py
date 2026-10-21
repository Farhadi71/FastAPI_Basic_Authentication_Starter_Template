
"""
Application entry point.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core import (
    settings,
    setup_logging,
)

from app.db import create_tables
from app.api import api_router
from app.middlewares import (
    RequestLoggingMiddleware,
    CorrelationIDMiddleware,
    RequestIDMiddleware,
)

setup_logging()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application startup and shutdown.
    """
    create_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(api_router)
