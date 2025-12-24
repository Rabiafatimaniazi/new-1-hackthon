from typing import Optional
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


class UserCreate(BaseModel):
    email: str
    name: Optional[str] = None
    background: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    background: Optional[str] = None