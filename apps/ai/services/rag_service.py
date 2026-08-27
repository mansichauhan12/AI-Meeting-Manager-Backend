from apps.meetings.services.ai_client import GeminiClient
from google import genai
from .vector_store_service import VectorStoreService

class RAGService:
    @staticmethod
    def ask_question(workspace_id: int, question: str) -> dict:
        # 1. Retrieve relevant chunks
        vector_store = VectorStoreService()
        results = vector_store.search_chunks(workspace_id=workspace_id, query=question, top_k=5)
        
        if not results:
            return {
                "answer": "No relevant meeting information found in this workspace.",
                "sources": []
            }
            
        # 2. Prepare context
        context_parts = []
        sources = []
        seen_meetings = set()
        
        for i, res in enumerate(results):
            text = res['text']
            meta = res['metadata']
            
            context_parts.append(f"Chunk {i+1}:\n{text}\n")
            
            meeting_id = meta.get('meeting_id')
            if meeting_id and meeting_id not in seen_meetings:
                seen_meetings.add(meeting_id)
                sources.append({
                    "meeting_id": meeting_id,
                    "chunk_id": meta.get('chunk_index')
                })
                
        context_str = "\n".join(context_parts)
        
        # 3. Call LLM
        prompt = (
            "Answer the question using ONLY the provided context.\n"
            "If the context does not contain the answer, say 'I don't know based on the provided context.'\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context_str}"
        )
        
        client = GeminiClient().get_client()
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.0,
            )
        )
        
        return {
            "answer": response.text,
            "sources": sources
        }
