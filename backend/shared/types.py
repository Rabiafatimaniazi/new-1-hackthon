from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class User(BaseModel):
    id: Optional[UUID] = None
    email: str
    name: Optional[str] = None
    background: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Chapter(BaseModel):
    id: Optional[UUID] = None
    title: str
    slug: str
    content: str
    urdu_content: Optional[str] = None
    order_index: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Section(BaseModel):
    id: Optional[UUID] = None
    chapter_id: UUID
    title: str
    content: str
    urdu_content: Optional[str] = None
    order_index: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChapterInteraction(BaseModel):
    id: Optional[UUID] = None
    user_id: UUID
    chapter_id: UUID
    last_accessed: Optional[datetime] = None
    progress_percentage: float = 0.0
    personalized_content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ChatQuery(BaseModel):
    query: str
    user_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, Any]]


class PersonalizationRequest(BaseModel):
    user_background: str
    content: str


class TranslationRequest(BaseModel):
    content: str
    preserve_formatting: bool = True


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    main_concepts: List[str]
    takeaways: List[str]


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]