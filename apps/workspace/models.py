from django.conf import settings
from django.db import models

from .choices import (
    WorkspaceRole,
    WorkspaceMemberStatus
)


class Workspace(models.Model):

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_workspaces"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "workspaces"

        ordering = ["-created_at"]

    def __str__(self):

        return self.name


class WorkspaceMember(models.Model):

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspace_memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=WorkspaceRole.choices,
        default=WorkspaceRole.MEMBER
    )

    status = models.CharField(
        max_length=20,
        choices=WorkspaceMemberStatus.choices,
        default=WorkspaceMemberStatus.ACTIVE
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "workspace_members"

        unique_together = ("workspace", "user")

    def __str__(self):

        return f"{self.user.email} - {self.workspace.name}"