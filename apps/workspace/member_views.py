from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .selectors import (
    WorkspaceSelector,
    WorkspaceMemberSelector,
)

from .serializers import (
    AddWorkspaceMemberSerializer,
    UpdateMemberRoleSerializer,
    WorkspaceMemberSerializer,
)

from .services import WorkspaceMemberService

from .access import WorkspaceAccessService


class WorkspaceMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        workspace = WorkspaceSelector.workspace_detail(

            request.user,

            request.data["workspace"]

        )

        if not WorkspaceAccessService.is_admin(
            workspace,
            request.user,
        ):
            return Response(
                {"message": "Permission denied"},
                status=403,
            )

        serializer = AddWorkspaceMemberSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        member = WorkspaceMemberService.add_member(

            workspace,

            serializer.validated_data

        )

        return Response(

            WorkspaceMemberSerializer(member).data,

            status=201,
        )

    def get(self, request, workspace_id):

        workspace = WorkspaceSelector.workspace_detail(

            request.user,

            workspace_id

        )

        members = WorkspaceMemberSelector.members(
            workspace
        )

        return Response(

            WorkspaceMemberSerializer(
                members,
                many=True
            ).data
        )

class WorkspaceMemberRoleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        member = WorkspaceMemberSelector.member(pk)

        serializer = UpdateMemberRoleSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        WorkspaceMemberService.update_role(

            member,

            serializer.validated_data["role"]

        )

        return Response({

            "message": "Role Updated"

        })

    def delete(self, request, pk):

     member = WorkspaceMemberSelector.member(pk)

     WorkspaceMemberService.remove_member(
        member
     )

     return Response({
         "message": "Member Removed"
        })