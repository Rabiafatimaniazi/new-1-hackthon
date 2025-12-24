from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Section(BaseModel):
    id: Optional[UUID] = None
    chapter_id: UUID
    title: str
    content: str
    urdu_content: Optional[str] = None
    order_index: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SectionCreate(BaseModel):
    chapter_id: UUID
    title: str
    content: str
    order_index: int


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    urdu_content: Optional[str] = None
    order_index: Optional[int] = None


class ContentChunk(BaseModel):
    id: Optional[UUID] = None
    chapter_id: UUID
    section_id: Optional[UUID] = None
    content: str
    heading_hierarchy: Optional[str] = None
    original_position: int
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None