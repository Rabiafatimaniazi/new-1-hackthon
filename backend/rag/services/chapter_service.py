from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from backend.rag.models.chapter import Chapter, ChapterCreate, ChapterUpdate
from backend.rag.core.logging_config import get_logger

logger = get_logger(__name__)

class ChapterService:
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would connect to a database
        self.chapters: List[Chapter] = []
        self._initialize_sample_chapters()

    def _initialize_sample_chapters(self):
        """Initialize with sample chapters for the Physical AI & Humanoid Robotics textbook"""
        sample_chapters = [
            Chapter(
                id=uuid4(),
                title="Introduction to Physical AI",
                slug="introduction-to-physical-ai",
                content="# Introduction to Physical AI\n\nPhysical AI represents the convergence of artificial intelligence and physical systems. This chapter introduces the fundamental concepts...",
                urdu_content="# جسمانی ای آئی کا تعارف\n\nجسمانی ای آئی مصنوعی ذہانت اور جسمانی نظاموں کے اتحاد کی نمائندگی کرتا ہے۔ یہ باب بنیادی تصورات کا تعارف کرائے گا...",
                order_index=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Chapter(
                id=uuid4(),
                title="Fundamentals of Humanoid Robotics",
                slug="fundamentals-of-humanoid-robotics",
                content="# Fundamentals of Humanoid Robotics\n\nHumanoid robots are designed to mimic human form and behavior. This chapter covers the essential components...",
                urdu_content="# انسان نما روبوٹکس کے بنیادیات\n\nانسان نما روبوٹس کو انسانی شکل اور رویے کی نقل کرنے کے لیے ڈیزائن کیا گیا ہے۔ یہ باب ضروری اجزاء کو دیکھے گا...",
                order_index=2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Chapter(
                id=uuid4(),
                title="Sensors and Perception",
                slug="sensors-and-perception",
                content="# Sensors and Perception\n\nPerception systems enable robots to understand their environment. This chapter explores various sensor technologies...",
                urdu_content="# سینسرز اور ادراک\n\nادراک کے نظام روبوٹس کو اپنے ماحول کو سمجھنے کے قابل بناتے ہیں۔ یہ باب مختلف سینسر ٹیکنالوجیز کا جائزہ لے گا...",
                order_index=3,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        self.chapters = sample_chapters
        logger.info(f"Initialized {len(self.chapters)} sample chapters")

    async def get_all_chapters(self) -> List[Chapter]:
        """Get all chapters ordered by index"""
        return sorted(self.chapters, key=lambda x: x.order_index)

    async def get_chapter_by_id(self, chapter_id: UUID) -> Optional[Chapter]:
        """Get a specific chapter by ID"""
        for chapter in self.chapters:
            if chapter.id == chapter_id:
                return chapter
        return None

    async def get_chapter_by_slug(self, slug: str) -> Optional[Chapter]:
        """Get a specific chapter by slug"""
        for chapter in self.chapters:
            if chapter.slug == slug:
                return chapter
        return None

    async def create_chapter(self, chapter_data: ChapterCreate) -> Chapter:
        """Create a new chapter"""
        chapter = Chapter(
            id=uuid4(),
            title=chapter_data.title,
            slug=chapter_data.slug,
            content=chapter_data.content,
            order_index=chapter_data.order_index,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.chapters.append(chapter)
        logger.info(f"Created chapter: {chapter.title} (ID: {chapter.id})")
        return chapter

    async def update_chapter(self, chapter_id: UUID, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """Update an existing chapter"""
        for i, chapter in enumerate(self.chapters):
            if chapter.id == chapter_id:
                update_data = chapter_data.dict(exclude_unset=True)
                updated_chapter = chapter.copy(update=update_data)
                updated_chapter.updated_at = datetime.utcnow()
                self.chapters[i] = updated_chapter
                logger.info(f"Updated chapter: {updated_chapter.title} (ID: {updated_chapter.id})")
                return updated_chapter
        return None

    async def delete_chapter(self, chapter_id: UUID) -> bool:
        """Delete a chapter"""
        for i, chapter in enumerate(self.chapters):
            if chapter.id == chapter_id:
                del self.chapters[i]
                logger.info(f"Deleted chapter with ID: {chapter_id}")
                return True
        return False

# Global instance
chapter_service = ChapterService()