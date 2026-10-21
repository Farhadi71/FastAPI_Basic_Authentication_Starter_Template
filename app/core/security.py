
"""
Authentication and security utilities.
"""

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings


security = HTTPBasic()


def verify_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(security),
    ],
) -> str:
    """
    Validate HTTP Basic Authentication credentials.
    """

    username_valid = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        settings.BASIC_AUTH_USERNAME.encode("utf-8"),
    )

    password_valid = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        settings.BASIC_AUTH_PASSWORD.encode("utf-8"),
    )

    if not (username_valid and password_valid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
