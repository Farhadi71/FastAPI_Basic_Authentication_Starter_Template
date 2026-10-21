"""
Application logging configuration.
"""

import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "propagate": True,
        },
        "uvicorn.error": {
            "level": "INFO",
            "propagate": True,
        },
        "uvicorn.access": {
            "level": "INFO",
            "propagate": False,
            "handlers": [],
        },
        "sqlalchemy.engine": {
            "level": "WARNING",
            "propagate": True,
        },
    },
}


def setup_logging() -> None:
    """
    Configure application logging.
    """
    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module.
    """
    return logging.getLogger(name)
