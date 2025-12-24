from typing import List, Dict, Any
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

class CitationService:
    def __init__(self):
        """Initialize the citation service"""
        logger.info("Citation service initialized")

    def format_citations(self, sources: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format sources into proper citations"""
        citations = []
        for i, source in enumerate(sources, 1):
            citation = {
                "id": f"source_{i}",
                "text": source.get("text", "")[:200] + "..." if len(source.get("text", "")) > 200 else source.get("text", ""),
                "relevance_score": f"{source.get('score', 0):.3f}",
                "chapter_id": source.get("chapter_id", ""),
                "section_id": source.get("section_id", ""),
                "position": str(source.get("original_position", i)),
                "full_text": source.get("text", "")
            }
            citations.append(citation)
        return citations

    def generate_citation_text(self, sources: List[Dict[str, Any]]) -> str:
        """Generate a human-readable citation text"""
        if not sources:
            return "No sources cited."

        citation_text = "Sources cited:\n"
        for i, source in enumerate(sources, 1):
            text_preview = source.get("text", "")[:100] + "..." if len(source.get("text", "")) > 100 else source.get("text", "")
            citation_text += f"{i}. Chapter ID: {source.get('chapter_id', 'N/A')}, Score: {source.get('score', 0):.3f}\n"
            citation_text += f"   Text preview: {text_preview}\n"

        return citation_text

    def validate_citations(self, sources: List[Dict[str, Any]]) -> bool:
        """Validate that citations are properly formatted and relevant"""
        if not sources:
            return True  # Empty sources list is valid

        for source in sources:
            if not isinstance(source, dict):
                logger.warning("Invalid source format: not a dictionary")
                return False

            required_fields = ['text', 'score']
            for field in required_fields:
                if field not in source:
                    logger.warning(f"Missing required field in source: {field}")
                    return False

            # Validate score is a number
            score = source.get('score')
            if not isinstance(score, (int, float)):
                logger.warning(f"Invalid score type in source: {type(score)}")
                return False

        return True

    def filter_citations_by_relevance(self, sources: List[Dict[str, Any]], threshold: float = 0.3) -> List[Dict[str, Any]]:
        """Filter citations by relevance score"""
        filtered_sources = [
            source for source in sources
            if source.get('score', 0) >= threshold
        ]
        logger.info(f"Filtered {len(sources)} sources to {len(filtered_sources)} based on relevance threshold {threshold}")
        return filtered_sources

# Global instance
citation_service = CitationService()