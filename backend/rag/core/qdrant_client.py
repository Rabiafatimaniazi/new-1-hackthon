from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from backend.rag.core.config import settings


class QdrantSetup:
    def __init__(self):
        # Initialize Qdrant client
        if settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            self.client = QdrantClient(url=settings.QDRANT_URL)

    def create_collection(self):
        """Create the textbook chunks collection if it doesn't exist"""
        # Check if collection already exists
        collections = self.client.get_collections()
        collection_names = [collection.name for collection in collections.collections]

        if settings.QDRANT_COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=models.Distance.COSINE
                ),
            )

            # Create payload index for chapter_id to optimize search
            self.client.create_payload_index(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                field_name="chapter_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

            print(f"Created collection: {settings.QDRANT_COLLECTION_NAME}")
        else:
            print(f"Collection {settings.QDRANT_COLLECTION_NAME} already exists")

    def add_textbook_chunks(self, chunks: List[Dict[str, Any]]):
        """Add textbook content chunks to the vector database"""
        points = []
        for i, chunk in enumerate(chunks):
            point = models.PointStruct(
                id=i,
                vector=chunk['vector'],
                payload={
                    "chapter_id": chunk.get('chapter_id', ''),
                    "section_id": chunk.get('section_id', ''),
                    "chunk_text": chunk['text'],
                    "original_position": chunk.get('position', i),
                    "heading_hierarchy": chunk.get('heading_hierarchy', '')
                }
            )
            points.append(point)

        # Upload points to the collection
        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=points
        )

    def search_chunks(self, query_vector: List[float], limit: int = 6) -> List[Dict[str, Any]]:
        """Search for relevant chunks based on query vector"""
        results = self.client.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            score_threshold=settings.SCORE_THRESHOLD
        )

        return [
            {
                "text": hit.payload["chunk_text"],
                "score": hit.score,
                "chapter_id": hit.payload.get("chapter_id", ""),
                "section_id": hit.payload.get("section_id", ""),
                "original_position": hit.payload.get("original_position", 0)
            }
            for hit in results
        ]


# Global instance
qdrant_setup = QdrantSetup()