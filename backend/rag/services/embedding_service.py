from typing import List
from sentence_transformers import SentenceTransformer
from backend.rag.core.config import settings
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

class EmbeddingService:
    def __init__(self):
        """Initialize the embedding model"""
        logger.info(f"Initializing embedding model: {settings.EMBEDDING_MODEL}")
        try:
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not text.strip():
            return [0.0] * settings.EMBEDDING_DIMENSION

        embedding = self.model.encode([text])[0].tolist()
        return embedding

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not texts:
            return []

        # Filter out empty texts but keep track of positions
        non_empty_texts = [text for text in texts if text.strip()]
        if not non_empty_texts:
            return [[0.0] * settings.EMBEDDING_DIMENSION] * len(texts)

        embeddings = self.model.encode(non_empty_texts).tolist()

        # Map back to original positions (fill empty texts with zero vectors)
        result = []
        non_empty_idx = 0
        for text in texts:
            if text.strip():
                result.append(embeddings[non_empty_idx])
                non_empty_idx += 1
            else:
                result.append([0.0] * settings.EMBEDDING_DIMENSION)

        return result

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a query (same as text but semantically different usage)"""
        return self.embed_text(query)

# Global instance
embedding_service = EmbeddingService()