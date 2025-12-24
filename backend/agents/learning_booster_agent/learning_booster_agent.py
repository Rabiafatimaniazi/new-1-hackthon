from typing import List, Dict, Any
from openai import OpenAI
import os
import json


class LearningBoosterAgent:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_learning_boosters(self, chapter_content: str, user_background: str = "intermediate") -> Dict[str, Any]:
        """Generate learning boosters based on chapter content and user background"""
        booster_prompt = f"""
        Generate learning boosters for the following chapter content based on the user's background level.

        User background: {user_background}
        Chapter content: {chapter_content}

        Provide the following in JSON format:
        - practice_exercises: Array of practice problems or exercises
        - key_terms: Array of important terms with definitions
        - common_mistakes: Array of common mistakes to avoid
        - additional_resources: Array of additional resources or readings
        - reflection_questions: Array of questions to promote deeper thinking
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": booster_prompt}],
            response_format={"type": "json_object"},
            max_tokens=1200
        )

        return json.loads(response.choices[0].message.content)

    def generate_practice_exercises(self, chapter_content: str, difficulty: str = "medium") -> List[str]:
        """Generate practice exercises based on chapter content"""
        exercise_prompt = f"""
        Generate 5 practice exercises based on the following chapter content.
        Difficulty level: {difficulty}

        Chapter content: {chapter_content}

        Return as an array of exercise descriptions.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": exercise_prompt}],
            response_format={"type": "json_object"},
            max_tokens=800
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("exercises", [])

    def generate_key_terms_summary(self, chapter_content: str) -> Dict[str, str]:
        """Generate a summary of key terms with definitions"""
        terms_prompt = f"""
        Extract and define the 10 most important terms from the following chapter content.

        Chapter content: {chapter_content}

        Return as a JSON object with terms as keys and definitions as values.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": terms_prompt}],
            response_format={"type": "json_object"},
            max_tokens=800
        )

        return json.loads(response.choices[0].message.content)


# Global instance
learning_booster_agent = LearningBoosterAgent()