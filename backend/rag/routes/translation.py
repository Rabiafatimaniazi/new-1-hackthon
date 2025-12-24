from fastapi import APIRouter
from backend.shared.types import TranslationRequest
from backend.rag.services.translation_service import UrduTranslationService
from backend.rag.services.markdown_preservation import markdown_preservation_service
from backend.rag.core.logging_config import get_logger

router = APIRouter(prefix="/translation", tags=["translation"])

# Initialize translation service
translation_service = UrduTranslationService()
logger = get_logger(__name__)


@router.post("/urdu")
async def translate_to_urdu(translation_request: TranslationRequest):
    """Translate content to Urdu"""
    logger.info(f"Received translation request with formatting preservation: {translation_request.preserve_formatting}")

    if translation_request.preserve_formatting:
        # Use markdown preservation service
        translated_content = markdown_preservation_service.translate_content_preserving_formatting(
            translation_request.content
        )
    else:
        # Use basic translation service
        translated_content = translation_service.translate_content(
            translation_request.content,
            translation_request.preserve_formatting
        )

    logger.info("Translation completed successfully")
    return {"translated_content": translated_content}


@router.post("/urdu/blocks")
async def translate_to_urdu_by_blocks(translation_request: TranslationRequest):
    """Translate content to Urdu by blocks to preserve formatting"""
    logger.info("Received translation request by blocks")

    # Use block-based translation to preserve formatting
    translated_content = markdown_preservation_service.translate_by_blocks(
        translation_request.content
    )

    logger.info("Block-based translation completed successfully")
    return {"translated_content": translated_content}