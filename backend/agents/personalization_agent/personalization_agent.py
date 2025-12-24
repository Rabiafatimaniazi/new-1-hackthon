from backend.rag.services.personalization_service import PersonalizationService


class PersonalizationAgent:
    def __init__(self):
        self.personalization_service = PersonalizationService()

    def adapt_for_user(self, content: str, user_profile: dict) -> str:
        """Adapt content based on user profile"""
        user_background = user_profile.get("background", "")
        return self.personalization_service.personalize_content(content, user_background)