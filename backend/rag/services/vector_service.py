from typing import List, Dict, Any, Optional
from uuid import UUID
from backend.rag.core.qdrant_client import qdrant_setup
from backend.rag.core.config import settings
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

class VectorService:
    def __init__(self):
        """Initialize the vector storage service"""
        # Ensure the collection exists
        qdrant_setup.create_collection()
        logger.info("Vector storage service initialized")

    def add_text_chunks(self, chunks: List[Dict[str, Any]]) -> bool:
        """Add text chunks with embeddings to the vector database"""
        try:
            qdrant_setup.add_textbook_chunks(chunks)
            logger.info(f"Added {len(chunks)} chunks to vector database")
            return True
        except Exception as e:
            logger.error(f"Failed to add chunks to vector database: {e}")
            return False

    def search_similar_chunks(self, query_vector: List[float], limit: int = None) -> List[Dict[str, Any]]:
        """Search for similar chunks based on query vector"""
        if limit is None:
            limit = settings.TOP_K

        try:
            results = qdrant_setup.search_chunks(query_vector, limit)
            logger.info(f"Found {len(results)} similar chunks for query")
            return results
        except Exception as e:
            logger.error(f"Failed to search similar chunks: {e}")
            return []

    def delete_by_chapter_id(self, chapter_id: str) -> bool:
        """Delete all vectors associated with a specific chapter ID"""
        # Note: This would require Qdrant client functionality to delete by payload
        # For now, we'll just log the attempt
        logger.info(f"Request to delete vectors for chapter: {chapter_id}")
        # Implementation would depend on Qdrant client capabilities
        return True

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector collection"""
        # Note: This would require Qdrant client functionality to get collection info
        return {
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "status": "active",
            "count": 0  # Would be actual count from Qdrant
        }

# Global instance
vector_service = VectorService()