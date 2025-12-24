from typing import List
from openai import OpenAI
import os
import json
from backend.shared.types import QuizQuestion, QuizResponse


class QuizAgent:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_quiz(self, chapter_content: str, difficulty: str = "medium") -> QuizResponse:
        """Generate quiz questions based on chapter content"""
        quiz_prompt = f"""
        Generate 5 multiple-choice questions based on the following chapter content.
        Difficulty level: {difficulty}
        Format each question as JSON with fields: question, options (array), correct_answer, explanation

        Chapter content: {chapter_content}
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": quiz_prompt}],
            response_format={"type": "json_object"},
            max_tokens=1500
        )

        questions_data = json.loads(response.choices[0].message.content)

        # Convert to QuizQuestion objects
        questions = []
        for q_data in questions_data:
            question = QuizQuestion(
                question=q_data["question"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"]
            )
            questions.append(question)

        return QuizResponse(questions=questions)