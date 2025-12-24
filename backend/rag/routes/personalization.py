from fastapi import APIRouter
from backend.rag.models.user_background import PersonalizationRequest as UserPersonalizationRequest
from backend.rag.services.personalization_service import PersonalizationService
from backend.rag.core.logging_config import get_logger

router = APIRouter(prefix="/personalization", tags=["personalization"])

# Initialize personalization service
personalization_service = PersonalizationService()
logger = get_logger(__name__)


@router.post("/adapt-content")
async def adapt_content(request: UserPersonalizationRequest):
    """Adapt content based on user background"""
    logger.info(f"Adapting content for background: {request.user_background}")

    adapted_content = personalization_service.personalize_content(
        request.content,
        request.user_background
    )

    logger.info("Content adaptation completed successfully")
    return {"adapted_content": adapted_content}


@router.post("/classify-background")
async def classify_background(background: str):
    """Classify user background into categories"""
    logger.info(f"Classifying background: {background}")

    classification = personalization_service.classify_user_background(background)

    logger.info(f"Background classified successfully: {classification}")
    return classification