from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.meetings.models import Meeting, ActionItem, Reminder
from apps.dashboard.services import DashboardService

def invalidate_dashboard_cache_for_workspace(workspace_id):
    if workspace_id:
        DashboardService.invalidate_cache(workspace_id)

@receiver(post_save, sender=Meeting)
@receiver(post_delete, sender=Meeting)
def meeting_changed(sender, instance, **kwargs):
    invalidate_dashboard_cache_for_workspace(instance.workspace_id)

@receiver(post_save, sender=ActionItem)
@receiver(post_delete, sender=ActionItem)
def action_item_changed(sender, instance, **kwargs):
    # Try to invalidate for the associated meeting's workspace
    if hasattr(instance, 'meeting') and instance.meeting:
        invalidate_dashboard_cache_for_workspace(instance.meeting.workspace_id)

@receiver(post_save, sender=Reminder)
@receiver(post_delete, sender=Reminder)
def reminder_changed(sender, instance, **kwargs):
    # Try to invalidate for the associated task's meeting's workspace
    if hasattr(instance, 'task') and instance.task and hasattr(instance.task, 'meeting') and instance.task.meeting:
        invalidate_dashboard_cache_for_workspace(instance.task.meeting.workspace_id)
