from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class Chapter(BaseModel):
    id: Optional[UUID] = None
    title: str
    slug: str
    content: str
    urdu_content: Optional[str] = None
    order_index: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChapterCreate(BaseModel):
    title: str
    slug: str
    content: str
    order_index: int


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    urdu_content: Optional[str] = None
    order_index: Optional[int] = None


class ChapterInteraction(BaseModel):
    id: Optional[UUID] = None
    user_id: UUID
    chapter_id: UUID
    last_accessed: Optional[datetime] = None
    progress_percentage: float = 0.0
    personalized_content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChapterInteractionCreate(BaseModel):
    user_id: UUID
    chapter_id: UUID
    progress_percentage: float = 0.0
    personalized_content: Optional[str] = None