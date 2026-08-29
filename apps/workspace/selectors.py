from .models import (
    Workspace,
    WorkspaceMember
)

from .choices import (
    WorkspaceMemberStatus
)


from django.shortcuts import get_object_or_404


class WorkspaceSelector:

    @staticmethod
    def user_workspaces(user):

        return Workspace.objects.filter(

            members__user=user,

            members__status=WorkspaceMemberStatus.ACTIVE,

            is_active=True

        ).select_related(
            "owner"
        ).distinct()

    @staticmethod
    def workspace_detail(user, workspace_id):

        return get_object_or_404(

            Workspace.objects.filter(

                members__user=user,

                members__status=WorkspaceMemberStatus.ACTIVE,

                is_active=True

            ).select_related("owner"),

            id=workspace_id

        )



class WorkspaceMemberSelector:

    @staticmethod
    def members(workspace):

        return WorkspaceMember.objects.filter(

            workspace=workspace,

            status__in=[WorkspaceMemberStatus.ACTIVE, WorkspaceMemberStatus.INVITED]

        ).select_related(
            "user"
        )

    @staticmethod
    def member(member_id):

        return WorkspaceMember.objects.select_related(

            "user",

            "workspace"

        ).get(id=member_id)