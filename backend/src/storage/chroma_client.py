"""ChromaDB client for vector storage and retrieval."""

import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class ChromaClient:
    """ChromaDB client wrapper for managing vector embeddings."""

    def __init__(self):
        """Initialize ChromaDB client."""
        self.client = chromadb.PersistentClient(
            path=settings.chroma_db_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )
        self.collection_name = "data_ghost_embeddings"
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        """Ensure the collection exists."""
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Data Ghost CSV embeddings"},
            )
            logger.info(f"ChromaDB collection '{self.collection_name}' ready")
        except Exception as e:
            logger.error(f"Error creating ChromaDB collection: {e}")
            raise

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add documents to the collection.

        Args:
            documents: List of document texts
            metadatas: List of metadata dictionaries
            ids: List of document IDs (optional)

        Returns:
            List of document IDs
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        try:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
            logger.info(f"Added {len(documents)} documents to ChromaDB")
            return ids
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
            raise

    def query(
        self,
        query_texts: List[str],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Query the collection for similar documents.

        Args:
            query_texts: List of query texts
            n_results: Number of results to return
            where: Filter conditions

        Returns:
            Query results
        """
        try:
            results = self.collection.query(
                query_texts=query_texts, n_results=n_results, where=where
            )
            logger.info(f"Queried ChromaDB for {len(query_texts)} texts")
            return results
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}")
            raise

    def delete(self, ids: List[str]) -> None:
        """
        Delete documents by IDs.

        Args:
            ids: List of document IDs to delete
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from ChromaDB")
        except Exception as e:
            logger.error(f"Error deleting documents from ChromaDB: {e}")
            raise

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Collection information
        """
        try:
            count = self.collection.count()
            return {
                "name": self.collection_name,
                "document_count": count,
                "path": settings.chroma_db_path,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise
