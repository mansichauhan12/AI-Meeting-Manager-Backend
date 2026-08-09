from rest_framework import serializers

from .models import (
    Workspace,
    WorkspaceMember
)

from .choices import WorkspaceRole


class WorkspaceSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(
        source="owner.email"
    )

    total_members = serializers.SerializerMethodField()

    class Meta:

        model = Workspace

        fields = (

            "id",

            "name",

            "description",

            "owner",

            "total_members",

            "created_at"

        )

    def get_total_members(self, obj):

        return obj.members.filter(
            status="ACTIVE"
        ).count()


class WorkspaceCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Workspace

        fields = (

            "name",

            "description"

        )

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 3:

            raise serializers.ValidationError(
                "Workspace name is too short."
            )

        return value

class WorkspaceMemberSerializer(serializers.ModelSerializer):

    user_email = serializers.ReadOnlyField(
        source="user.email"
    )

    class Meta:

        model = WorkspaceMember

        fields = (

            "id",

            "user",

            "user_email",

            "role",

            "status",

            "joined_at"

        )


class AddWorkspaceMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=WorkspaceRole.choices, default=WorkspaceRole.MEMBER)

class UpdateMemberRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=WorkspaceRole.choices)