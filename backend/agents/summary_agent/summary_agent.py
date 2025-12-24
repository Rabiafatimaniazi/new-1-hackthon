from typing import Dict, List
from openai import OpenAI
import os
import json
from backend.shared.types import SummaryResponse


class SummaryAgent:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_summary(self, chapter_content: str) -> SummaryResponse:
        """Generate chapter summary with key points"""
        summary_prompt = f"""
        Create a concise summary of the following chapter content.
        Include 3-5 key points, main concepts, and important takeaways.
        Format as JSON with fields: summary, key_points, main_concepts, takeaways

        Chapter content: {chapter_content}
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}],
            response_format={"type": "json_object"},
            max_tokens=1000
        )

        result = json.loads(response.choices[0].message.content)

        return SummaryResponse(
            summary=result.get("summary", ""),
            key_points=result.get("key_points", []),
            main_concepts=result.get("main_concepts", []),
            takeaways=result.get("takeaways", [])
        )