from django.conf import settings
from django.db import models

from apps.workspace.models import Workspace

from .choices import (
    MeetingStatus,
    ActionItemStatus,
    ActionItemPriority,
    ReminderStatus,
)


class Meeting(models.Model):

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="meetings",
    )

    title = models.CharField(
        max_length=255
    )

    meeting_date = models.DateTimeField()

    audio_file = models.FileField(
        upload_to="meetings/audio/",
        blank=True,
        null=True,
    )

    file_name = models.CharField(
        max_length=255,
        blank=True,
    )

    transcript = models.TextField(
        blank=True,
        null=True,
    )

    summary = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=MeetingStatus.choices,
        default=MeetingStatus.UPLOADED,
    )

    error_message = models.TextField(
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_meetings",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "meetings"

        ordering = ["-meeting_date"]

        indexes = [
            models.Index(
                fields=["workspace", "-meeting_date"]
            ),
            models.Index(
                fields=["workspace", "status"]
            ),
        ]

    def __str__(self):

        return self.title


class ActionItem(models.Model):

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="action_items",
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_action_items",
    )

    deadline = models.DateTimeField(
        null=True,
        blank=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=ActionItemPriority.choices,
        default=ActionItemPriority.MEDIUM,
    )

    status = models.CharField(
        max_length=20,
        choices=ActionItemStatus.choices,
        default=ActionItemStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "action_items"

        ordering = ["deadline", "-created_at"]

    def __str__(self):

        return self.title


class Reminder(models.Model):

    task = models.ForeignKey(
        ActionItem,
        on_delete=models.CASCADE,
        related_name="reminders",
    )

    send_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=ReminderStatus.choices,
        default=ReminderStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "reminders"

        indexes = [
            models.Index(
                fields=["status", "send_at"]
            )
        ]

    def __str__(self):

        return f"{self.task.title} - {self.send_at}"