"""
utils/logger.py
================
Centralized logging configuration for the entire application.
"""

import logging
import sys
from pathlib import Path

import config


def _ensure_log_directory_exists() -> None:
    """Create the logs/ directory if it does not already exist."""
    Path(config.LOGS_DIR).mkdir(parents=True, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    Create (or retrieve) a configured logger instance.

    Parameters
    ----------
    name : str
        Name of the logger, conventionally passed as `__name__`.

    Returns
    -------
    logging.Logger
    """
    _ensure_log_directory_exists()

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(config.LOG_FORMAT)

    file_handler = logging.FileHandler(config.LOG_FILE_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger
