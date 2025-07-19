"""Health check router for API monitoring."""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from src.core.config import settings
from src.storage import ChromaClient, FileStorage

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with component status."""
    health_status = {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "components": {},
    }

    # Check ChromaDB
    try:
        chroma_client = ChromaClient()
        chroma_info = chroma_client.get_collection_info()
        health_status["components"]["chromadb"] = {
            "status": "healthy",
            "collection_count": chroma_info["document_count"],
        }
    except Exception as e:
        health_status["components"]["chromadb"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    # Check file storage
    try:
        file_storage = FileStorage()
        storage_info = file_storage.get_storage_info()
        health_status["components"]["file_storage"] = {
            "status": "healthy",
            "total_files": storage_info["total_files"],
            "total_size_mb": storage_info["total_size_mb"],
        }
    except Exception as e:
        health_status["components"]["file_storage"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        health_status["status"] = "degraded"

    return health_status
