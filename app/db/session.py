'''
app.db.session
'''
from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db import engine

session_local = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_db() -> Generator[Session, None, None]:
    """
    Provide database session for FastAPI dependencies.
    """

    db = session_local()

    try:
        yield db

    finally:
        db.close()