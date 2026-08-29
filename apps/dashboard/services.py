from django.core.cache import cache
from django.utils import timezone

from apps.meetings.models import Meeting, ActionItem, Reminder
from apps.meetings.choices import MeetingStatus, ActionItemStatus, ReminderStatus
from apps.dashboard.serializers import DashboardResponseSerializer


class DashboardService:
    CACHE_TIMEOUT = 60 * 15  # 15 minutes

    @staticmethod
    def get_dashboard_cache_key(workspace_id: int) -> str:
        return f"dashboard:workspace:{workspace_id}"

    @staticmethod
    def invalidate_cache(workspace_id: int):
        cache_key = DashboardService.get_dashboard_cache_key(workspace_id)
        cache.delete(cache_key)

    @classmethod
    def get_dashboard(cls, user, workspace):
        cache_key = cls.get_dashboard_cache_key(workspace.id)
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        now = timezone.now()

        # Statistics
        total_meetings = Meeting.objects.filter(workspace=workspace).count()
        completed_meetings = Meeting.objects.filter(workspace=workspace, status=MeetingStatus.COMPLETED).count()
        processing_meetings = Meeting.objects.filter(workspace=workspace, status=MeetingStatus.PROCESSING).count()
        failed_meetings = Meeting.objects.filter(workspace=workspace, status=MeetingStatus.FAILED).count()
        
        pending_tasks = ActionItem.objects.filter(
            meeting__workspace=workspace,
            status=ActionItemStatus.PENDING
        ).count()
        
        completed_tasks = ActionItem.objects.filter(
            meeting__workspace=workspace,
            status=ActionItemStatus.DONE
        ).count()

        upcoming_reminders_count = Reminder.objects.filter(
            task__meeting__workspace=workspace,
            status=ReminderStatus.PENDING,
            send_at__gte=now
        ).count()

        statistics = {
            "total_meetings": total_meetings,
            "completed_meetings": completed_meetings,
            "processing_meetings": processing_meetings,
            "failed_meetings": failed_meetings,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "upcoming_reminders": upcoming_reminders_count,
        }

        # Upcoming Meetings (future)
        upcoming_meetings_qs = Meeting.objects.filter(
            workspace=workspace,
            meeting_date__gte=now
        ).order_by("meeting_date")[:5]

        upcoming_meetings = [
            {
                "id": m.id,
                "title": m.title,
                "meeting_date": m.meeting_date,
            } for m in upcoming_meetings_qs
        ]

        # Recent Meetings (past)
        recent_meetings_qs = Meeting.objects.filter(
            workspace=workspace
        ).order_by("-created_at")[:5]

        recent_meetings = [
            {
                "id": m.id,
                "title": m.title,
                "status": m.status,
            } for m in recent_meetings_qs
        ]

        # Pending Action Items (for the current user ideally, but dashboard spec mentioned "preferably assigned_to=current_user")
        pending_tasks_qs = ActionItem.objects.filter(
            meeting__workspace=workspace,
            status=ActionItemStatus.PENDING,
            assigned_to=user
        ).order_by("deadline")[:5]

        pending_tasks_list = [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "deadline": t.deadline,
            } for t in pending_tasks_qs
        ]

        # Upcoming Reminders
        upcoming_reminders_qs = Reminder.objects.filter(
            task__meeting__workspace=workspace,
            status=ReminderStatus.PENDING,
            send_at__gte=now
        ).select_related("task").order_by("send_at")[:5]

        upcoming_reminders_list = [
            {
                "id": r.id,
                "task_title": r.task.title,
                "send_at": r.send_at,
            } for r in upcoming_reminders_qs
        ]

        data = {
            "statistics": statistics,
            "upcoming_meetings": upcoming_meetings,
            "pending_tasks": pending_tasks_list,
            "upcoming_reminders": upcoming_reminders_list,
            "recent_meetings": recent_meetings,
        }
        
        serializer = DashboardResponseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        # Cache for 15 minutes
        cache.set(cache_key, validated_data, cls.CACHE_TIMEOUT)
        
        return validated_data
