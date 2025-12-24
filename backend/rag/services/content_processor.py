from typing import List, Dict, Any
import re
from backend.rag.services.rag_service import RAGService


class ContentProcessor:
    def __init__(self):
        self.rag_service = RAGService()

    def chunk_textbook_content(self, content: str, chapter_id: str, max_chunk_size: int = 500) -> List[Dict[str, Any]]:
        """Split textbook content into chunks for vector storage"""
        # Split content by headings
        heading_pattern = r'(^|\n)(#{1,6})\s+(.+?)(?=\n|$)'
        parts = re.split(heading_pattern, content)

        chunks = []
        current_heading = ""
        current_text = ""

        i = 0
        while i < len(parts):
            part = parts[i]

            # Check if this part is a heading
            if part and part.startswith('#'):
                # Save the previous chunk if it exists
                if current_text.strip():
                    chunks.extend(self._create_chunks_from_text(current_text, chapter_id, current_heading))

                # Extract heading
                if i + 2 < len(parts):
                    current_heading = f"{parts[i]} {parts[i+2]}".strip()
                    i += 3
                else:
                    current_heading = part.strip()
                    i += 1
                current_text = ""
            else:
                current_text += part
                i += 1

        # Add the last chunk if it exists
        if current_text.strip():
            chunks.extend(self._create_chunks_from_text(current_text, chapter_id, current_heading))

        return chunks

    def _create_chunks_from_text(self, text: str, chapter_id: str, heading: str) -> List[Dict[str, Any]]:
        """Create chunks from a section of text"""
        chunks = []

        # Split text into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        current_chunk = ""
        for paragraph in paragraphs:
            # Check if adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > 500 and current_chunk:
                # Save current chunk
                chunks.append({
                    'text': current_chunk.strip(),
                    'chapter_id': chapter_id,
                    'heading_hierarchy': heading,
                    'position': len(chunks)
                })
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'chapter_id': chapter_id,
                'heading_hierarchy': heading,
                'position': len(chunks)
            })

        return chunks

    def process_and_store_chapters(self, chapters: List[Dict[str, Any]]):
        """Process and store all chapters in the vector database"""
        all_chunks = []

        for chapter in chapters:
            chapter_id = chapter['id']
            content = chapter['content']

            # Chunk the content
            chunks = self.chunk_textbook_content(content, chapter_id)
            all_chunks.extend(chunks)

        # Add all chunks to the RAG system
        self.rag_service.add_document_chunks(all_chunks)

        return len(all_chunks)