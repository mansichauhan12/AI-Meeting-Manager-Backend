from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.workspace.models import Workspace

from .exceptions import MeetingNotFoundException
from .permissions import IsActionItemAuthorized
from .serializers import (
    MeetingUploadSerializer,
    MeetingListSerializer,
    MeetingDetailSerializer,
    ActionItemSerializer,
    ActionItemCreateUpdateSerializer,
)
from .selectors import MeetingSelector, ActionItemSelector
from .services.meeting_service import MeetingService
from .services.action_item_service import ActionItemService

class MeetingUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request):

        serializer = MeetingUploadSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        workspace_id = serializer.validated_data[
            "workspace"
        ].id

        try:

            workspace = Workspace.objects.get(
                id=workspace_id
            )

        except Workspace.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Workspace not found.",
                    "error_code": "WORKSPACE_NOT_FOUND",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        meeting = MeetingService.create_meeting(
            user=request.user,
            workspace=workspace,
            title=serializer.validated_data["title"],
            meeting_date=serializer.validated_data[
                "meeting_date"
            ],
            audio_file=serializer.validated_data[
                "audio_file"
            ],
        )

        return Response(
            {
                "success": True,
                "message": "Meeting uploaded successfully.",
                "data": {
                    "id": meeting.id,
                    "title": meeting.title,
                    "status": meeting.status,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class MeetingListAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        workspace_id = request.query_params.get(
            "workspace"
        )

        meetings = MeetingSelector.get_user_meetings(
            user=request.user,
            workspace_id=workspace_id,
        )

        serializer = MeetingListSerializer(
            meetings,
            many=True,
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class MeetingDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, pk):

        meeting = MeetingSelector.get_meeting(
            user=request.user,
            meeting_id=pk,
        )

        if not meeting:

            raise MeetingNotFoundException()

        serializer = MeetingDetailSerializer(
            meeting
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    def delete(self, request, pk):

        meeting = MeetingSelector.get_meeting(
            user=request.user,
            meeting_id=pk,
        )

        if not meeting:

            raise MeetingNotFoundException()

        MeetingService.delete_meeting(
            user=request.user,
            meeting=meeting,
        )

        return Response(
            {
                "success": True,
                "message": "Meeting deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class ActionItemListCreateAPIView(APIView):

    permission_classes = [
        IsActionItemAuthorized,
    ]

    def get(self, request):
        workspace_id = request.query_params.get("workspace")
        action_items = ActionItemSelector.get_action_items(
            user=request.user,
            workspace_id=workspace_id,
        )
        serializer = ActionItemSerializer(action_items, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ActionItemCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_item = ActionItemService.create_action_item(
            serializer.validated_data
        )

        response_serializer = ActionItemSerializer(action_item)
        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ActionItemDetailAPIView(APIView):

    permission_classes = [
        IsActionItemAuthorized,
    ]

    def get(self, request, pk):
        action_item = ActionItemSelector.get_action_item(
            user=request.user,
            action_item_id=pk,
        )
        if not action_item:
            return Response({"success": False, "message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, action_item)

        serializer = ActionItemSerializer(action_item)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        action_item = ActionItemSelector.get_action_item(
            user=request.user,
            action_item_id=pk,
        )
        if not action_item:
            return Response({"success": False, "message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, action_item)

        serializer = ActionItemCreateUpdateSerializer(
            action_item, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)

        action_item = ActionItemService.update_action_item(
            action_item, serializer.validated_data
        )

        response_serializer = ActionItemSerializer(action_item)
        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk):
        action_item = ActionItemSelector.get_action_item(
            user=request.user,
            action_item_id=pk,
        )
        if not action_item:
            return Response({"success": False, "message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, action_item)

        serializer = ActionItemCreateUpdateSerializer(
            action_item, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        action_item = ActionItemService.update_action_item(
            action_item, serializer.validated_data
        )

        response_serializer = ActionItemSerializer(action_item)
        return Response(
            {
                "success": True,
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        action_item = ActionItemSelector.get_action_item(
            user=request.user,
            action_item_id=pk,
        )
        if not action_item:
            return Response({"success": False, "message": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, action_item)

        ActionItemService.delete_action_item(action_item)
        
        return Response(
            {
                "success": True,
                "message": "Action item deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )

