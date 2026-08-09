from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    WorkspaceSerializer,
    WorkspaceCreateSerializer
)

from .selectors import WorkspaceSelector

from .services import WorkspaceService

from .permissions import IsWorkspaceOwner


class WorkspaceListCreateAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return WorkspaceSelector.user_workspaces(
            self.request.user
        )

    def get_serializer_class(self):

        if self.request.method == "POST":

            return WorkspaceCreateSerializer

        return WorkspaceSerializer

    def list(self, request, *args, **kwargs):

        serializer = WorkspaceSerializer(
            self.get_queryset(),
            many=True
        )

        return Response({

            "success": True,

            "count": len(serializer.data),

            "data": serializer.data

        })

    def create(self, request, *args, **kwargs):

        serializer = WorkspaceCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        workspace = WorkspaceService.create_workspace(
            request.user,
            serializer.validated_data
        )

        return Response({

            "success": True,

            "message": "Workspace created successfully.",

            "data": WorkspaceSerializer(workspace).data

        }, status=status.HTTP_201_CREATED)


class WorkspaceDetailAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [
        IsAuthenticated,
        IsWorkspaceOwner
    ]

    serializer_class = WorkspaceSerializer

    def get_object(self):

        workspace = WorkspaceSelector.workspace_detail(
            self.request.user,
            self.kwargs["pk"]
        )

        self.check_object_permissions(
            self.request,
            workspace
        )

        return workspace

    def retrieve(self, request, *args, **kwargs):

        return Response({

            "success": True,

            "data": WorkspaceSerializer(
                self.get_object()
            ).data

        })

    def update(self, request, *args, **kwargs):

        workspace = self.get_object()

        serializer = WorkspaceCreateSerializer(

            workspace,

            data=request.data

        )

        serializer.is_valid(
            raise_exception=True
        )

        workspace = WorkspaceService.update_workspace(

            workspace,

            serializer.validated_data

        )

        return Response({

            "success": True,

            "message": "Workspace updated successfully.",

            "data": WorkspaceSerializer(
                workspace
            ).data

        })

    def destroy(self, request, *args, **kwargs):

        WorkspaceService.soft_delete_workspace(
            self.get_object()
        )

        return Response({

            "success": True,

            "message": "Workspace deleted successfully."

        })