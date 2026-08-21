from rest_framework import serializers

from .models import (
    Meeting,
    ActionItem,
)


class MeetingUploadSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Meeting

        fields = (
            "workspace",
            "title",
            "meeting_date",
            "audio_file",
        )

        extra_kwargs = {
            "audio_file": {
                "required": True,
            }
        }

    def validate_title(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Meeting title cannot be empty."
            )

        return value


class ActionItemSerializer(
    serializers.ModelSerializer
):

    assigned_to_name = serializers.CharField(
        source="assigned_to.full_name",
        read_only=True,
        default=None,
    )

    class Meta:

        model = ActionItem

        fields = (
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_name",
            "deadline",
            "priority",
            "status",
            "created_at",
        )


class ActionItemCreateUpdateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ActionItem

        fields = (
            "meeting",
            "title",
            "description",
            "assigned_to",
            "deadline",
            "priority",
            "status",
        )


class MeetingListSerializer(
    serializers.ModelSerializer
):

    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    class Meta:

        model = Meeting

        fields = (
            "id",
            "title",
            "meeting_date",
            "status",
            "file_name",
            "created_by",
            "created_by_name",
            "created_at",
        )


class MeetingDetailSerializer(
    serializers.ModelSerializer
):

    action_items = ActionItemSerializer(
        many=True,
        read_only=True,
    )

    created_by_name = serializers.CharField(
        source="created_by.full_name",
        read_only=True,
    )

    workspace_name = serializers.CharField(
        source="workspace.name",
        read_only=True,
    )

    class Meta:

        model = Meeting

        fields = (
            "id",
            "workspace",
            "workspace_name",
            "title",
            "meeting_date",
            "audio_file",
            "file_name",
            "transcript",
            "summary",
            "status",
            "error_message",
            "created_by",
            "created_by_name",
            "action_items",
            "created_at",
            "updated_at",
        )