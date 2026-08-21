from google import genai
from django.conf import settings


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_client(self):
        return self.client