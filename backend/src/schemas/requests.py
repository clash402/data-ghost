"""Request schemas for API endpoints."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AskQueryRequest(BaseModel):
    """Request schema for asking questions about CSV data."""

    question: str = Field(..., description="The question to ask about the data")
    context: Optional[Dict[str, Any]] = Field(
        None, description="Additional context data about the CSV"
    )
    session_id: Optional[str] = Field(
        None, description="Session identifier for conversation continuity"
    )


class UploadRequest(BaseModel):
    """Request schema for file upload metadata."""

    description: Optional[str] = Field(
        None, description="Optional description of the uploaded file"
    )
    tags: Optional[list[str]] = Field(
        default_factory=list, description="Tags for categorizing the file"
    )
