from django.urls import path

from .views import (
    MeetingUploadAPIView,
    MeetingListAPIView,
    MeetingDetailAPIView,
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

]