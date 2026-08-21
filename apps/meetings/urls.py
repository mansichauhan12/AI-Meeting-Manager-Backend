from django.urls import path

from .views import (
    MeetingUploadAPIView,
    MeetingListAPIView,
    MeetingDetailAPIView,
    ActionItemListCreateAPIView,
    ActionItemDetailAPIView,
)


urlpatterns = [

    path(
        "",
        MeetingListAPIView.as_view(),
        name="meeting-list",
    ),

    path(
        "upload/",
        MeetingUploadAPIView.as_view(),
        name="meeting-upload",
    ),

    path(
        "<int:pk>/",
        MeetingDetailAPIView.as_view(),
        name="meeting-detail",
    ),

    path(
        "action-items/",
        ActionItemListCreateAPIView.as_view(),
        name="action-item-list",
    ),

    path(
        "action-items/<int:pk>/",
        ActionItemDetailAPIView.as_view(),
        name="action-item-detail",
    ),

]