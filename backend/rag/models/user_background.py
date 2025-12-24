from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class BackgroundLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    RESEARCHER = "researcher"


class UserBackground(BaseModel):
    id: Optional[str] = None
    user_id: str
    level: BackgroundLevel
    interests: list[str] = []
    experience_years: Optional[float] = None
    preferred_learning_style: Optional[str] = None  # e.g., "visual", "textual", "hands-on"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserBackgroundCreate(BaseModel):
    user_id: str
    level: BackgroundLevel
    interests: list[str] = []
    experience_years: Optional[float] = None
    preferred_learning_style: Optional[str] = None


class UserBackgroundUpdate(BaseModel):
    level: Optional[BackgroundLevel] = None
    interests: Optional[list[str]] = None
    experience_years: Optional[float] = None
    preferred_learning_style: Optional[str] = None


class PersonalizationRequest(BaseModel):
    content: str
    user_background: str  # This would be the background level or description


class PersonalizationResponse(BaseModel):
    personalized_content: str
    original_background: str
    personalization_applied: bool = True