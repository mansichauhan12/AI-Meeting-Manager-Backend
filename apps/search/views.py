from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import SearchRequestSerializer
from apps.ai.services.vector_store_service import VectorStoreService
from apps.ai.services.rag_service import RAGService
from apps.workspace.models import Workspace

class SemanticSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        query = serializer.validated_data['query']
        workspace_id = serializer.validated_data['workspace_id']
        
        # Verify workspace access
        if not Workspace.objects.filter(id=workspace_id, members__user=request.user).exists():
            return Response({"success": False, "error": "Workspace not found or access denied."}, status=status.HTTP_403_FORBIDDEN)
            
        vector_store = VectorStoreService()
        results = vector_store.search_chunks(workspace_id=workspace_id, query=query, top_k=5)
        
        data = []
        for res in results:
            data.append({
                "meeting_id": res['metadata'].get('meeting_id'),
                "chunk": res['text'],
                "score": res.get('score')
            })
            
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        query = serializer.validated_data['query']
        workspace_id = serializer.validated_data['workspace_id']
        
        # Verify workspace access
        if not Workspace.objects.filter(id=workspace_id, members__user=request.user).exists():
            return Response({"success": False, "error": "Workspace not found or access denied."}, status=status.HTTP_403_FORBIDDEN)
            
        rag_service = RAGService()
        try:
            result = rag_service.ask_question(workspace_id=workspace_id, question=query)
            return Response({"success": True, "data": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
