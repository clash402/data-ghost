"""Query router for handling AI-powered questions about CSV data."""

import time
from fastapi import APIRouter, HTTPException
from typing import Optional

from src.core.logging import get_logger
from src.schemas.requests import AskQueryRequest
from src.schemas.responses import AskQueryResponse
from src.services import QueryService

logger = get_logger(__name__)
router = APIRouter(prefix="/ask", tags=["query"])


@router.post("/", response_model=AskQueryResponse)
async def ask_question(request: AskQueryRequest) -> AskQueryResponse:
    """
    Ask a question about uploaded CSV data.

    Args:
        request: Query request containing question and context

    Returns:
        AI-generated answer with confidence and sources
    """
    start_time = time.time()

    try:
        # Initialize query service
        query_service = QueryService()

        # Process the query
        answer, confidence, sources = await query_service.process_query(
            question=request.question,
            context=request.context,
            session_id=request.session_id,
        )

        processing_time = time.time() - start_time

        logger.info(f"Processed query: '{request.question}' in {processing_time:.2f}s")

        return AskQueryResponse(
            answer=answer,
            confidence=confidence,
            sources=sources,
            session_id=request.session_id,
            processing_time=processing_time,
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500, detail=f"Query processing failed: {str(e)}"
        )


@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get query history for a session."""
    try:
        query_service = QueryService()
        history = await query_service.get_session_history(session_id)
        return {"session_id": session_id, "queries": history}
    except Exception as e:
        logger.error(f"Error getting session history: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get session history: {str(e)}"
        )


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a session's history."""
    try:
        query_service = QueryService()
        await query_service.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to clear session: {str(e)}"
        )
