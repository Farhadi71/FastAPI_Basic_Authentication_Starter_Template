"""
app.api.endpoint.health
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy import text

from sqlalchemy.exc import SQLAlchemyError

from app.db import engine
from app.core import (
    get_logger,
    verify_basic_auth,
)


logger = get_logger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
def health_check(
    _: Annotated[str, Depends(verify_basic_auth)],
    ) -> dict[str, str]:
    """
    Check whether the API is running.
    """
    logger.info("API health check requested")

    return {
        "status": "ok",
        "message": "API is running",
    }

@router.get("/db")
def database_health_check():

    """
    Check whether the database connection is available.
    """
    logger.info("Database health check succeeded")

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
        }

    except SQLAlchemyError as exc:
        logger.exception("Database health check failed")
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "error",
                "database": "unavailable",
            },
        ) from exc
