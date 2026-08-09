from django.urls import path

from .views import (
    WorkspaceListCreateAPIView,
    WorkspaceDetailAPIView

)
from .member_views import *

urlpatterns = [

    path(
        "",
        WorkspaceListCreateAPIView.as_view(),
        name="workspace-list"
    ),

    path(
        "<int:pk>/",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-detail"
    ),

     path(
        "<int:workspace_id>/members/",
        WorkspaceMemberAPIView.as_view()
    ),

    path(
        "members/",
        WorkspaceMemberAPIView.as_view()
    ),

    path(
        "members/<int:pk>/role/",
        WorkspaceMemberRoleAPIView.as_view()
    ),

    path(
        "members/<int:pk>/",
        WorkspaceMemberRoleAPIView.as_view()
    ),
]