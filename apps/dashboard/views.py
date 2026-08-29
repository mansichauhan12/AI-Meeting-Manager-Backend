from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.workspace.models import Workspace, WorkspaceMember
from apps.dashboard.services import DashboardService

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        
        if not workspace_id:
            return Response(
                {"success": False, "error": "workspace_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        workspace = get_object_or_404(Workspace, id=workspace_id)
        
        # Check permissions
        is_member = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user
        ).exists()
        
        if not is_member:
            return Response(
                {"success": False, "error": "You do not have access to this workspace."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            dashboard_data = DashboardService.get_dashboard(request.user, workspace)
            
            return Response({
                "success": True,
                "data": dashboard_data
            })
            
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
