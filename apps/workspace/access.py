from .models import WorkspaceMember
from .choices import (
    WorkspaceRole,
    WorkspaceMemberStatus,
)


class WorkspaceAccessService:

    @staticmethod
    def membership(workspace, user):
        return WorkspaceMember.objects.filter(
            workspace=workspace,
            user=user,
            status=WorkspaceMemberStatus.ACTIVE
        ).first()

    @staticmethod
    def is_member(workspace, user):
        return WorkspaceAccessService.membership(
            workspace,
            user
        ) is not None

    @staticmethod
    def is_admin(workspace, user):

        membership = WorkspaceAccessService.membership(
            workspace,
            user
        )

        if not membership:
            return False

        return membership.role in [
            WorkspaceRole.OWNER,
            WorkspaceRole.ADMIN,
        ]

    @staticmethod
    def is_owner(workspace, user):

        membership = WorkspaceAccessService.membership(
            workspace,
            user
        )

        if not membership:
            return False

        return membership.role == WorkspaceRole.OWNER