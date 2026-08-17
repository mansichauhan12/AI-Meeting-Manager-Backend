from django.contrib import admin

from .models import (
    Meeting,
    ActionItem,
    Reminder,
)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "workspace",
        "created_by",
        "meeting_date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "meeting_date",
    )

    search_fields = (
        "title",
        "transcript",
        "summary",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "meeting",
        "assigned_to",
        "priority",
        "status",
        "deadline",
    )

    list_filter = (
        "priority",
        "status",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "task",
        "send_at",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )