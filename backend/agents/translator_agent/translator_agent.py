from backend.rag.services.translation_service import UrduTranslationService


class TranslatorAgent:
    def __init__(self):
        self.translation_service = UrduTranslationService()

    def translate_to_urdu(self, content: str) -> str:
        """Translate content to Urdu with preserved formatting"""
        return self.translation_service.translate_content(content, preserve_formatting=True)