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