"""File utility functions for CSV processing."""

import os
import csv
from typing import Optional
from pathlib import Path

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


def validate_csv_file(file_path: str) -> bool:
    """
    Validate that a file is a proper CSV file.

    Args:
        file_path: Path to the file to validate

    Returns:
        True if valid CSV, False otherwise
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Try to read the first few lines to validate CSV format
            reader = csv.reader(file)
            header = next(reader, None)

            if not header:
                logger.warning(f"CSV file {file_path} appears to be empty")
                return False

            # Check if we have at least one data row
            first_row = next(reader, None)
            if not first_row:
                logger.warning(f"CSV file {file_path} has no data rows")
                return False

            return True

    except Exception as e:
        logger.error(f"Error validating CSV file {file_path}: {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.

    Args:
        file_path: Path to the file

    Returns:
        File extension (lowercase, without dot)
    """
    return Path(file_path).suffix.lower().lstrip(".")


def ensure_upload_directory() -> str:
    """
    Ensure the upload directory exists and return its path.

    Returns:
        Path to the upload directory
    """
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return str(upload_dir)


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in bytes
    """
    return os.path.getsize(file_path)


def is_file_size_valid(file_path: str) -> bool:
    """
    Check if a file size is within the allowed limit.

    Args:
        file_path: Path to the file

    Returns:
        True if file size is valid, False otherwise
    """
    file_size = get_file_size(file_path)
    return file_size <= settings.max_file_size


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, "_")

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[: 255 - len(ext)] + ext

    return filename
