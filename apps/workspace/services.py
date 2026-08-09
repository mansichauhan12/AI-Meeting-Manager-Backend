from django.db import transaction

from .models import (
    Workspace,
    WorkspaceMember
)

from .choices import (
    WorkspaceRole,
    WorkspaceMemberStatus
)
from django.contrib.auth import get_user_model

from .exceptions import (
    MemberAlreadyExists,
    MemberNotFound,
)

User = get_user_model()


class WorkspaceService:

    @staticmethod
    @transaction.atomic
    def create_workspace(user, validated_data):

        workspace = Workspace.objects.create(
            owner=user,
            **validated_data
        )

        WorkspaceMember.objects.create(
            workspace=workspace,
            user=user,
            role=WorkspaceRole.OWNER,
            status=WorkspaceMemberStatus.ACTIVE
        )

        return workspace

    @staticmethod
    @transaction.atomic
    def update_workspace(workspace, validated_data):

        for field, value in validated_data.items():

            setattr(workspace, field, value)

        workspace.save()

        return workspace

    @staticmethod
    @transaction.atomic
    def soft_delete_workspace(workspace):

        workspace.is_active = False

        workspace.save(
            update_fields=["is_active"]
        )

        return workspace


class WorkspaceMemberService:

    @staticmethod
    @transaction.atomic
    def add_member(
        workspace,
        validated_data,
    ):

        email = validated_data["email"]

        role = validated_data["role"]

        try:
            user = User.objects.get(email=email)
            status = WorkspaceMemberStatus.ACTIVE
        except User.DoesNotExist:
            import uuid
            import secrets
            user = User.objects.create_user(
                username=f"{email.split('@')[0]}_{uuid.uuid4().hex[:6]}",
                email=email,
                password=secrets.token_urlsafe(16)
            )
            status = WorkspaceMemberStatus.INVITED

        exists = WorkspaceMember.objects.filter(
            workspace=workspace,
            user=user,
            status=WorkspaceMemberStatus.ACTIVE
        ).exists()

        if exists:
            raise MemberAlreadyExists()

        return WorkspaceMember.objects.create(

            workspace=workspace,

            user=user,

            role=role,

            status=status
        )

    @staticmethod
    def update_role(member, role):

        member.role = role

        member.save(
            update_fields=["role"]
        )

        return member

    @staticmethod
    def remove_member(member):

        member.status = WorkspaceMemberStatus.REMOVED

        member.save(
            update_fields=["status"]
        )

        return member