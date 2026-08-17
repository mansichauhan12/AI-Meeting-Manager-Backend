from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.workspace.models import Workspace

from .exceptions import MeetingNotFoundException
from .serializers import (
    MeetingUploadSerializer,
    MeetingListSerializer,
    MeetingDetailSerializer,
)
from .selectors import MeetingSelector
from .services import MeetingService

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

