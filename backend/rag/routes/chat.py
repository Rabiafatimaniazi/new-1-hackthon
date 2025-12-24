from fastapi import APIRouter, Depends
from typing import List
from backend.shared.types import ChatQuery, ChatResponse
from backend.rag.services.rag_service import RAGService
from backend.rag.services.citation_service import citation_service
from backend.rag.core.logging_config import get_logger

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize services
rag_service = RAGService()
logger = get_logger(__name__)


@router.post("/query", response_model=ChatResponse)
async def query_chat(query: ChatQuery):
    """Main chat endpoint with RAG"""
    logger.info(f"Received chat query: {query.query[:50]}...")
    try:
        response = rag_service.query(query.query)

        # Format citations for the response
        formatted_sources = citation_service.format_citations(response.sources)
        response.sources = formatted_sources

        logger.info("Chat query processed successfully")
        return response
    except Exception as e:
        logger.error(f"Error processing chat query: {e}")
        return ChatResponse(
            response="Sorry, I encountered an error while processing your query.",
            sources=[]
        )


@router.get("/history")
async def get_chat_history():
    """Get chat history for user"""
    # This would require user authentication and database storage
    # For now, returning an empty history
    return {"history": []}


@router.delete("/clear")
async def clear_chat_history():
    """Clear chat history"""
    # This would require user authentication and database operations
    # For now, returning a success message
    return {"message": "Chat history cleared"}