# from rest_framework.permissions import BasePermission

# from apps.workspace.models import WorkspaceMember


# class IsWorkspaceMember(BasePermission):
#     """
#     Allows access only to active members
#     of the requested workspace.
#     """

#     def has_permission(self, request, view):

#         if not request.user.is_authenticated:
#             return False

#         workspace_id = (
#             request.data.get("workspace")
#             or request.query_params.get("workspace")
#             or view.kwargs.get("workspace_id")
#         )

#         if not workspace_id:
#             return True

#         return WorkspaceMember.objects.filter(
#             workspace_id=workspace_id,
#             user=request.user,
#             is_active=True,
#         ).exists()

from rest_framework.permissions import BasePermission

from apps.workspace.models import WorkspaceMember


class IsAuthenticatedUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )


def user_is_workspace_member(user, workspace_id):

    return WorkspaceMember.objects.filter(
        workspace_id=workspace_id,
        user=user,
        status="ACTIVE",
    ).exists()


class IsActionItemAuthorized(BasePermission):
    """
    Permission for Action Items:
    - Must be authenticated
    - Read: Workspace Member
    - Update: Assigned User OR Admin/Owner
    - Delete: Admin/Owner
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == "POST":
            # For POST, check if user is in workspace given meeting_id
            meeting_id = request.data.get("meeting")
            if not meeting_id:
                return True # handled by serializer validation

            from apps.meetings.models import Meeting
            try:
                meeting = Meeting.objects.get(id=meeting_id)
            except Meeting.DoesNotExist:
                return True

            return WorkspaceMember.objects.filter(
                workspace=meeting.workspace,
                user=request.user,
                status="ACTIVE",
            ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        workspace = obj.meeting.workspace
        member = WorkspaceMember.objects.filter(
            workspace=workspace, user=request.user, status="ACTIVE"
        ).first()

        if not member:
            return False

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        is_admin_or_owner = member.role in ["ADMIN", "OWNER"]

        if request.method in ["PUT", "PATCH"]:
            return is_admin_or_owner or (obj.assigned_to == request.user)

        if request.method == "DELETE":
            return is_admin_or_owner

        return False