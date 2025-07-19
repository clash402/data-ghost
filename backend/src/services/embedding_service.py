"""Embedding service for creating vector embeddings of text."""

from typing import List, Dict, Any
import openai

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """Service for creating and managing text embeddings."""

    def __init__(self):
        """Initialize embedding service."""
        self.client = openai.OpenAI(api_key=settings.openai_api_key)

    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small", input=texts
            )

            embeddings = [embedding.embedding for embedding in response.data]
            logger.info(f"Created embeddings for {len(texts)} texts")

            return embeddings

        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            raise

    async def create_single_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        embeddings = await self.create_embeddings([text])
        return embeddings[0]

    async def batch_create_embeddings(
        self, texts: List[str], batch_size: int = 100
    ) -> List[List[float]]:
        """
        Create embeddings in batches.

        Args:
            texts: List of texts to embed
            batch_size: Size of each batch

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_embeddings = await self.create_embeddings(batch)
            all_embeddings.extend(batch_embeddings)

            logger.info(
                f"Processed batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}"
            )

        return all_embeddings
