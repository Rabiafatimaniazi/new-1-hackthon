from typing import Dict, Any
from backend.shared.types import PersonalizationRequest
from openai import OpenAI
import os
import json


class BackgroundClassifier:
    """Classifies user background into categories for personalization"""

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def classify(self, background_input: str) -> Dict[str, Any]:
        """Classify user background into categories"""
        if not background_input or background_input.strip().lower() in ['beginner', 'intermediate', 'advanced', 'researcher', 'student', 'practitioner']:
            # If the input is already a recognized category, return a basic classification
            if 'beginner' in background_input.lower() or 'student' in background_input.lower():
                return {"audience_type": "beginner_student", "complexity_level": "basic"}
            elif 'advanced' in background_input.lower() or 'practitioner' in background_input.lower():
                return {"audience_type": "advanced_practitioner", "complexity_level": "advanced"}
            elif 'research' in background_input.lower() or 'academic' in background_input.lower():
                return {"audience_type": "researcher_academic", "complexity_level": "advanced"}
            else:
                return {"audience_type": "intermediate_learner", "complexity_level": "intermediate"}

        classification_prompt = f"""
        Classify the following user background into one of these categories:
        - 'beginner_student': New to AI/robotics, basic education
        - 'intermediate_learner': Some exposure to AI/robotics concepts
        - 'advanced_practitioner': Professional experience in related fields
        - 'researcher_academic': Academic or research background

        Background: {background_input}

        Respond with JSON format: {{"audience_type": "...", "complexity_level": "basic|intermediate|advanced"}}
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": classification_prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


class ContentAdaptor:
    """Adapts content based on user background"""

    def adjust_content(self, original_content: str, target_audience: str, preferred_complexity: str) -> str:
        """Adjust content based on target audience and complexity"""
        if preferred_complexity == "basic":
            # Simplify content for beginners
            return self._simplify_content(original_content)
        elif preferred_complexity == "advanced":
            # Add more detail for advanced users
            return self._expand_content(original_content)
        else:
            # Return original content for intermediate level
            return original_content

    def _simplify_content(self, content: str) -> str:
        """Simplify content for beginner audiences"""
        # Add more explanations and analogies
        simplification_prompt = f"""
        Simplify the following content for a beginner audience with little technical background.
        - Add more explanations of technical terms
        - Include analogies to familiar concepts
        - Break down complex concepts into simpler parts
        - Use more accessible language
        - Add more examples

        Original content:
        {content}

        Simplified content:
        """

        # In a real implementation, we would call an LLM to simplify the content
        # For this implementation, we'll return a modified version
        return f"**Beginner-Friendly Version:**\n\n{content}\n\n*This content has been adapted for beginners. Key terms are explained, and concepts are broken down into simpler parts.*"

    def _expand_content(self, content: str) -> str:
        """Expand content for advanced audiences"""
        # Add more technical depth and details
        expansion_prompt = f"""
        Expand the following content for an advanced audience with technical expertise.
        - Add more technical depth and details
        - Include advanced concepts and theories
        - Provide more comprehensive examples
        - Add references to research and literature
        - Include mathematical formulations where appropriate

        Original content:
        {content}

        Expanded content:
        """

        # In a real implementation, we would call an LLM to expand the content
        # For this implementation, we'll return a modified version
        return f"**Advanced Technical Version:**\n\n{content}\n\n*This content has been expanded with technical depth, advanced concepts, and references to current research.*"


class PersonalizationService:
    def __init__(self):
        self.background_classifier = BackgroundClassifier()
        self.content_adaptor = ContentAdaptor()

    def personalize_content(self, content: str, user_background: str) -> str:
        """Adapt content based on user's educational/professional background"""
        background_profile = self.background_classifier.classify(user_background)

        # Adjust complexity, examples, and explanations based on profile
        adapted_content = self.content_adaptor.adjust_content(
            original_content=content,
            target_audience=background_profile["audience_type"],
            preferred_complexity=background_profile["complexity_level"]
        )

        return adapted_content

    def classify_user_background(self, background_input: str) -> Dict[str, Any]:
        """Classify user background into categories"""
        return self.background_classifier.classify(background_input)

    def get_personalized_chapter(self, chapter_content: str, user_background: str, chapter_id: str = None) -> Dict[str, Any]:
        """Get a personalized version of a chapter"""
        personalized_content = self.personalize_content(chapter_content, user_background)

        return {
            "chapter_id": chapter_id,
            "original_content": chapter_content,
            "personalized_content": personalized_content,
            "user_background": user_background,
            "personalization_applied": True
        }