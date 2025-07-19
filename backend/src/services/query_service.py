"""Query service for processing AI-powered questions about CSV data."""

import json
from typing import Tuple, List, Optional, Dict, Any
import openai

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class QueryService:
    """Service for processing queries about CSV data."""

    def __init__(self):
        """Initialize query service."""
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        # In a real implementation, you'd have session storage here
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    async def process_query(
        self,
        question: str,
        context: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Tuple[str, float, List[str]]:
        """
        Process a query about CSV data.

        Args:
            question: The question to ask
            context: CSV data context
            session_id: Session identifier

        Returns:
            Tuple of (answer, confidence, sources)
        """
        try:
            # Prepare the prompt
            prompt = self._build_prompt(question, context)

            # Get response from OpenAI
            response = await self._get_openai_response(prompt)

            # Extract answer and confidence
            answer = response.choices[0].message.content
            confidence = 0.85  # Placeholder confidence score

            # Store in session if provided
            if session_id:
                self._store_in_session(session_id, question, answer)

            return answer, confidence, []

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    def _build_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Build the prompt for OpenAI."""
        base_prompt = """You are a helpful AI assistant that analyzes CSV data. 
        Answer questions about the data in a clear, concise manner.
        
        Question: {question}
        """

        if context:
            base_prompt += f"\nData Context:\n{context}\n"

        base_prompt += "\nPlease provide a helpful answer based on the data."

        return base_prompt.format(question=question)

    async def _get_openai_response(self, prompt: str):
        """Get response from OpenAI."""
        return self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant for analyzing CSV data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

    def _store_in_session(self, session_id: str, question: str, answer: str):
        """Store query in session history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {
                "question": question,
                "answer": answer,
                "timestamp": "2024-01-01T00:00:00Z",  # Placeholder timestamp
            }
        )

    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get session history."""
        return self.sessions.get(session_id, [])

    async def clear_session(self, session_id: str):
        """Clear session history."""
        if session_id in self.sessions:
            del self.sessions[session_id]
