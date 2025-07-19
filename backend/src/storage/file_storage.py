"""File storage utilities for handling uploaded files."""

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from src.core.config import settings
from src.core.logging import get_logger
from src.utils.file_utils import ensure_upload_directory, sanitize_filename

logger = get_logger(__name__)


class FileStorage:
    """File storage manager for uploaded files."""

    def __init__(self):
        """Initialize file storage."""
        self.upload_dir = ensure_upload_directory()
        logger.info(f"File storage initialized at: {self.upload_dir}")

    def save_uploaded_file(
        self,
        file_content: bytes,
        original_filename: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Save an uploaded file to storage.

        Args:
            file_content: File content as bytes
            original_filename: Original filename
            metadata: Additional metadata

        Returns:
            File information dictionary
        """
        # Generate unique filename
        file_id = str(uuid.uuid4())
        safe_filename = sanitize_filename(original_filename)
        file_extension = Path(safe_filename).suffix

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{file_id}{file_extension}"
        file_path = Path(self.upload_dir) / new_filename

        try:
            # Save file
            with open(file_path, "wb") as f:
                f.write(file_content)

            # Get file info
            file_size = len(file_content)
            file_info = {
                "file_id": file_id,
                "original_filename": original_filename,
                "stored_filename": new_filename,
                "file_path": str(file_path),
                "file_size": file_size,
                "file_extension": file_extension.lstrip("."),
                "upload_timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
            }

            logger.info(
                f"Saved file: {original_filename} -> {new_filename} ({file_size} bytes)"
            )
            return file_info

        except Exception as e:
            logger.error(f"Error saving file {original_filename}: {e}")
            raise

    def get_file_path(self, file_id: str) -> Optional[str]:
        """
        Get the file path for a given file ID.

        Args:
            file_id: File ID to look up

        Returns:
            File path if found, None otherwise
        """
        # This is a simplified implementation
        # In a real application, you'd want to maintain a database of file mappings
        for file_path in Path(self.upload_dir).glob(f"*_{file_id}.*"):
            return str(file_path)
        return None

    def delete_file(self, file_id: str) -> bool:
        """
        Delete a file by its ID.

        Args:
            file_id: File ID to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        file_path = self.get_file_path(file_id)
        if file_path and Path(file_path).exists():
            try:
                Path(file_path).unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            except Exception as e:
                logger.error(f"Error deleting file {file_path}: {e}")
                return False
        return False

    def list_files(self) -> list[Dict[str, Any]]:
        """
        List all stored files.

        Returns:
            List of file information dictionaries
        """
        files = []
        for file_path in Path(self.upload_dir).glob("*"):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    files.append(
                        {
                            "filename": file_path.name,
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(
                                stat.st_mtime
                            ).isoformat(),
                            "path": str(file_path),
                        }
                    )
                except Exception as e:
                    logger.warning(f"Error getting file info for {file_path}: {e}")

        return files

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get storage information.

        Returns:
            Storage information dictionary
        """
        total_files = 0
        total_size = 0

        for file_path in Path(self.upload_dir).glob("*"):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size

        return {
            "upload_directory": self.upload_dir,
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }
