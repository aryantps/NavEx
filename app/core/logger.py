import os
import sys
import logging
from logging.config import dictConfig
from app.core.context import get_request_id
from app.core.config import settings

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id() or "-"
        return True

if settings.USE_UVICORN_LOGGER:
    try:
        from uvicorn.main import logger as uvicorn_logger
        logger = uvicorn_logger
    except ImportError:
        logger = logging.getLogger("uvicorn")
else:
    LOG_LEVEL = settings.LOG_LEVEL.upper()
    LOG_FORMAT = "[%(asctime)s] %(levelname)-2s [%(request_id)s] %(name)s - %(message)s"

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {
            "request_id": {
                '()': RequestIDFilter,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "filters": ["request_id"],
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "app": {
                "level": LOG_LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
        },
        "root": {
            "level": LOG_LEVEL,
            "handlers": ["default"],
        },
    }

    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")