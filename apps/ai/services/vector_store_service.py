import chromadb
from django.conf import settings
import os

from .embedding_service import EmbeddingService

class VectorStoreService:
    def __init__(self):
        # We store ChromaDB data locally in the project root
        persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "meetings_collection"
        
        # We manually handle embeddings with our EmbeddingService
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def add_chunks(self, workspace_id: int, meeting_id: int, chunks: list[str]):
        if not chunks:
            return

        embeddings = EmbeddingService.get_embeddings(chunks)
        
        ids = [f"workspace_{workspace_id}_meeting_{meeting_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "workspace_id": workspace_id,
                "meeting_id": meeting_id,
                "chunk_index": i
            } for i in range(len(chunks))
        ]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=chunks
        )

# In apps/ai/services/vector_store_service.py

    def search_chunks(self, workspace_id: int, query: str, top_k: int = 5, distance_threshold: float = 0.8) -> list[dict]:
        query_embedding = EmbeddingService.get_embedding(query.lower())
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"workspace_id": workspace_id}
        )
        
        parsed_results = []
        if results and results.get('documents') and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                distance = results['distances'][0][i] if 'distances' in results and results['distances'] else None
                
                # Filter out chunks that exceed our maximum distance threshold
                if distance is not None and distance > distance_threshold:
                    continue
                    
                parsed_results.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": distance
                })
                
        return parsed_results
