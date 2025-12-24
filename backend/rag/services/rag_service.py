from typing import List, Dict, Any
from openai import OpenAI
import os
from backend.shared.types import ChatQuery, ChatResponse
from backend.rag.core.config import settings
from backend.rag.services.embedding_service import embedding_service
from backend.rag.services.vector_service import vector_service
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

class RAGService:
    def __init__(self):
        # Initialize OpenAI client
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable must be set")
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        logger.info("RAGService initialized successfully")

    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query using embeddings and vector search"""
        try:
            # Generate embedding for the query
            query_embedding = embedding_service.embed_query(query)

            # Search for similar chunks in the vector database
            results = vector_service.search_similar_chunks(
                query_vector=query_embedding,
                limit=settings.TOP_K
            )
            logger.info(f"Retrieved {len(results)} relevant chunks for query")
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []

    def generate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """Generate response using retrieved context"""
        if not context:
            return "I cannot answer based on the provided textbook content."

        # Format context with scores and sources
        context_str = "\n".join([
            f"Source {i+1} (relevance: {item['score']:.2f}): {item['text']}"
            for i, item in enumerate(context)
        ])

        prompt = f"""
        Answer the following question based ONLY on the provided context from the textbook.
        If the answer cannot be found in the context, say "I cannot answer based on the provided textbook content."
        Be helpful, accurate, and cite which sources you used to answer the question.

        Context:
        {context_str}

        Question: {query}

        Answer: """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            logger.info("Response generated successfully")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating the response."

    def query(self, query: str) -> ChatResponse:
        """Main query method that combines embedding, retrieval, and generation"""
        logger.info(f"Processing query: {query[:50]}...")

        # Retrieve relevant context
        context = self.retrieve_context(query)

        # Generate response
        response_text = self.generate_response(query, context)

        # Prepare sources for response
        sources = [
            {
                "text": item["text"],
                "score": item["score"],
                "chapter_id": item["chapter_id"],
                "section_id": item["section_id"],
                "original_position": item["original_position"]
            }
            for item in context
        ]

        logger.info("Query processed successfully")
        return ChatResponse(response=response_text, sources=sources)

    def add_document_chunks(self, chunks: List[Dict[str, Any]]):
        """Add document chunks to the vector database with embeddings"""
        try:
            # Process chunks to add embeddings
            enhanced_chunks = []
            for chunk in chunks:
                text = chunk['text']
                embedding = embedding_service.embed_text(text)
                enhanced_chunk = {
                    'vector': embedding,
                    'text': text,
                    'chapter_id': chunk.get('chapter_id', ''),
                    'section_id': chunk.get('section_id', ''),
                    'position': chunk.get('position', 0),
                    'heading_hierarchy': chunk.get('heading_hierarchy', '')
                }
                enhanced_chunks.append(enhanced_chunk)

            # Add to vector database
            success = vector_service.add_text_chunks(enhanced_chunks)
            if success:
                logger.info(f"Successfully added {len(enhanced_chunks)} chunks to vector database")
            else:
                logger.error("Failed to add chunks to vector database")
        except Exception as e:
            logger.error(f"Error adding document chunks: {e}")