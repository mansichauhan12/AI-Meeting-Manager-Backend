from apps.meetings.services.ai_client import GeminiClient

class EmbeddingService:
    @staticmethod
    def get_embedding(text: str) -> list[float]:
        client = GeminiClient().get_client()
        response = client.models.embed_content(
            model='gemini-embedding-2',
            contents=text
        )
        # For a single text input, the response has embeddings[0].values
        if hasattr(response, 'embeddings') and response.embeddings:
            return response.embeddings[0].values
        
        raise Exception("Failed to generate embedding.")

    @staticmethod
    def get_embeddings(texts: list[str]) -> list[list[float]]:
        client = GeminiClient().get_client()
        response = client.models.embed_content(
            model='gemini-embedding-2',
            contents=texts
        )
        if hasattr(response, 'embeddings') and response.embeddings:
            return [emb.values for emb in response.embeddings]
            
        raise Exception("Failed to generate embeddings.")
