"""Logging configuration for the Data Ghost backend."""

import logging
import sys
from typing import Any

from src.core.config import settings


def setup_logging() -> None:
    """Configure logging for the application."""

    # Create logger
    logger = logging.getLogger("data_ghost")
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    # Set logging level for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(f"data_ghost.{name}")


# Initialize logging when module is imported
setup_logging()
