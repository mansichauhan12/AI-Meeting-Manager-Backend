from rest_framework.permissions import BasePermission

from .access import WorkspaceAccessService


class IsWorkspaceOwner(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return WorkspaceAccessService.is_owner(
            obj,
            request.user
        )


class IsWorkspaceAdmin(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return WorkspaceAccessService.is_admin(
            obj,
            request.user
        )