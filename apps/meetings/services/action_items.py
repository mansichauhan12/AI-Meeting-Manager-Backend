import json

from .ai_client import GeminiClient
from google import genai


class ActionItemService:

    @staticmethod
    def extract_action_items(transcript):

        client = GeminiClient().get_client()
        
        prompt = """
You are a meeting action-item extraction assistant.

Extract actionable tasks from the meeting transcript.

Return ONLY valid JSON.

Expected format:

{
    "action_items": [
        {
            "title": "string",
            "description": "string",
            "priority": "LOW",
            "assignee_name": "string (or null if not assigned)"
        }
    ]
}

Priority must be one of:

LOW
MEDIUM
HIGH

If there are no action items, return:

{
    "action_items": []
}

Here is the transcript:
"""
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[prompt, transcript],
            config=genai.types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json"
            )
        )

        return json.loads(response.text)