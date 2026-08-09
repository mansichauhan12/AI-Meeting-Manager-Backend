from django.contrib import admin

from .models import (
    Workspace,
    WorkspaceMember
)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "owner",
        "is_active",
        "created_at"
    )

    search_fields = (
        "name",
        "owner__email"
    )


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):

    list_display = (
        "workspace",
        "user",
        "role",
        "status",
        "joined_at"
    )

    search_fields = (
        "workspace__name",
        "user__email"
    )

    list_filter = (
        "role",
        "status"
    )