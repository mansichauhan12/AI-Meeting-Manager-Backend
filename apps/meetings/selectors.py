from django.db.models import QuerySet

from .models import Meeting


class MeetingSelector:

    @staticmethod
    def get_user_meetings(
        user,
        workspace_id=None,
    ) -> QuerySet:

        queryset = (
            Meeting.objects
            .select_related(
                "workspace",
                "created_by",
            )
            .prefetch_related(
                "action_items__assigned_to",
            )
            .filter(
                workspace__members__user=user,
                workspace__members__status="ACTIVE",
            )
            .distinct()
        )

        if workspace_id:
            queryset = queryset.filter(
                workspace_id=workspace_id
            )

        return queryset

    @staticmethod
    def get_meeting(
        user,
        meeting_id,
    ):

        return (
            Meeting.objects
            .select_related(
                "workspace",
                "created_by",
            )
            .prefetch_related(
                "action_items__assigned_to",
                "action_items__reminders",
            )
            .filter(
                id=meeting_id,
                workspace__members__user=user,
                workspace__members__status="ACTIVE",
            )
            .first()
        )