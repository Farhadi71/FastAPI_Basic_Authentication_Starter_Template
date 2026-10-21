
"""
API v1 router configuration.
"""

from fastapi import APIRouter

from app.api.endpoint.v1.health import router as health_router


router = APIRouter()

router.include_router(health_router)
