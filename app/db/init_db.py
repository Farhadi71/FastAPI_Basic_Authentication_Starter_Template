"""
app.db.init_db
Database initialization utilities.
"""

import app.models  # noqa: F401

from app.db import Base, engine


def create_tables() -> None:
    """
    Create database tables that do not already exist.
    """
    Base.metadata.create_all(bind=engine)
