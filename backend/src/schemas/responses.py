"""Response schemas for API endpoints."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class AskQueryResponse(BaseModel):
    """Response schema for query answers."""

    answer: str = Field(..., description="The answer to the question")
    confidence: Optional[float] = Field(None, description="Confidence score (0-1)")
    sources: Optional[list[str]] = Field(
        default_factory=list, description="Sources used for the answer"
    )
    session_id: Optional[str] = Field(None, description="Session identifier")
    processing_time: Optional[float] = Field(
        None, description="Time taken to process the query"
    )


class UploadResponse(BaseModel):
    """Response schema for file uploads."""

    success: bool = Field(..., description="Whether the upload was successful")
    message: str = Field(..., description="Status message")
    file_id: Optional[str] = Field(
        None, description="Unique identifier for the uploaded file"
    )
    file_name: Optional[str] = Field(None, description="Name of the uploaded file")
    file_size: Optional[int] = Field(
        None, description="Size of the uploaded file in bytes"
    )
    data_summary: Optional[dict[str, Any]] = Field(
        None, description="Summary of the uploaded data"
    )


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_code: Optional[str] = Field(
        None, description="Error code for client handling"
    )
