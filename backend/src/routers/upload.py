"""Upload router for handling CSV file uploads."""

import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional

from src.core.logging import get_logger
from src.schemas.responses import UploadResponse
from src.storage import FileStorage
from src.services import CSVService
from src.utils.file_utils import validate_csv_file, get_file_extension

logger = get_logger(__name__)
router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
) -> UploadResponse:
    """
    Upload a CSV file for analysis.

    Args:
        file: CSV file to upload
        description: Optional description of the file
        tags: Optional comma-separated tags

    Returns:
        Upload response with file information
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        file_extension = get_file_extension(file.filename)
        if file_extension != "csv":
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Expected CSV, got {file_extension.upper()}",
            )

        # Read file content
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")

        # Save file
        file_storage = FileStorage()
        metadata = {
            "description": description,
            "tags": tags.split(",") if tags else [],
            "original_filename": file.filename,
        }

        file_info = file_storage.save_uploaded_file(
            file_content=file_content,
            original_filename=file.filename,
            metadata=metadata,
        )

        # Parse and analyze CSV
        csv_service = CSVService()
        csv_data = csv_service.parse_csv(file_info["file_path"])

        # Generate data summary
        data_summary = {
            "total_rows": csv_data["total_rows"],
            "total_columns": csv_data["total_columns"],
            "headers": csv_data["headers"],
            "column_stats": csv_data["column_stats"],
            "summary": csv_service.generate_summary(csv_data),
        }

        logger.info(f"Successfully uploaded and processed CSV: {file.filename}")

        return UploadResponse(
            success=True,
            message="File uploaded and processed successfully",
            file_id=file_info["file_id"],
            file_name=file_info["original_filename"],
            file_size=file_info["file_size"],
            data_summary=data_summary,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/files")
async def list_uploaded_files():
    """List all uploaded files."""
    try:
        file_storage = FileStorage()
        files = file_storage.list_files()
        return {"files": files, "total_count": len(files)}
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file."""
    try:
        file_storage = FileStorage()
        success = file_storage.delete_file(file_id)

        if success:
            return {"message": f"File {file_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"File {file_id} not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
