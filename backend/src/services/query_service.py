"""Query service for processing natural language queries about CSV data."""

from typing import List, Dict, Any, Optional
import openai

from src.core.config import settings
from src.core.logging import get_logger
from src.storage import ChromaClient

logger = get_logger(__name__)


class QueryService:
    """Service for processing queries about uploaded CSV data."""

    def __init__(self):
        """Initialize query service."""
        if not settings.openai_api_key:
            logger.warning(
                "OpenAI API key not configured. Query service will be disabled."
            )
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.chroma_client = ChromaClient()

    async def process_query(
        self, question: str, context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process a natural language query about the data.

        Args:
            question: The question to ask
            context_data: Optional context data about the CSV

        Returns:
            Answer to the question
        """
        if not self.client:
            return "OpenAI API key not configured. Please configure the API key to use query functionality."

        try:
            # Build the prompt with context
            prompt = self._build_prompt(question, context_data)

            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful data analyst assistant. Answer questions about CSV data in a clear and concise manner.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )

            answer = response.choices[0].message.content
            logger.info(f"Processed query: {question[:50]}...")

            return answer

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    def _build_prompt(
        self, question: str, context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a prompt for the query.

        Args:
            question: The question to ask
            context_data: Optional context data

        Returns:
            Formatted prompt
        """
        prompt = f"Question: {question}\n\n"

        if context_data:
            prompt += f"Context:\n"
            if "headers" in context_data:
                prompt += f"Columns: {', '.join(context_data['headers'])}\n"
            if "total_rows" in context_data:
                prompt += f"Total rows: {context_data['total_rows']}\n"
            if "summary" in context_data:
                prompt += f"Data summary: {context_data['summary']}\n"

        prompt += (
            "\nPlease provide a clear and helpful answer based on the available data."
        )

        return prompt
