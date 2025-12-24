from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from backend.rag.models.chapter import Chapter, ChapterCreate, ChapterUpdate
from backend.rag.services.chapter_service import chapter_service

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.get("/", response_model=List[Chapter])
async def get_all_chapters():
    """Get all textbook chapters"""
    chapters = await chapter_service.get_all_chapters()
    return chapters


@router.get("/{chapter_id}", response_model=Chapter)
async def get_chapter_by_id(chapter_id: UUID):
    """Get a specific chapter by ID"""
    chapter = await chapter_service.get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return chapter


@router.get("/slug/{slug}", response_model=Chapter)
async def get_chapter_by_slug(slug: str):
    """Get a specific chapter by slug"""
    chapter = await chapter_service.get_chapter_by_slug(slug)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return chapter


@router.post("/", response_model=Chapter)
async def create_chapter(chapter_data: ChapterCreate):
    """Create a new chapter"""
    created_chapter = await chapter_service.create_chapter(chapter_data)
    return created_chapter


@router.put("/{chapter_id}", response_model=Chapter)
async def update_chapter(chapter_id: UUID, chapter_data: ChapterUpdate):
    """Update an existing chapter"""
    updated_chapter = await chapter_service.update_chapter(chapter_id, chapter_data)
    if not updated_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return updated_chapter


@router.delete("/{chapter_id}")
async def delete_chapter(chapter_id: UUID):
    """Delete a chapter"""
    success = await chapter_service.delete_chapter(chapter_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return {"message": "Chapter deleted successfully"}