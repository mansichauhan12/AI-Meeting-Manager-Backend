from .ai_client import GeminiClient
from google import genai


class SummarizationService:

    @staticmethod
    def generate_summary(transcript):

        client = GeminiClient().get_client()
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[
                "You are a professional meeting assistant. Summarize the meeting clearly. Focus on decisions, important discussions, and key takeaways.",
                "Here is the transcript:",
                transcript
            ],
            config=genai.types.GenerateContentConfig(
                temperature=0.2,
            )
        )

        return response.text