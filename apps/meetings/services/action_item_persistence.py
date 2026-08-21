from apps.meetings.models import ActionItem
from apps.meetings.choices import ActionItemPriority
from apps.workspace.models import WorkspaceMember


class ActionItemPersistenceService:

    @staticmethod
    def create_action_items(
        *,
        meeting,
        action_items,
    ):

        created_items = []

        for item in action_items:

            priority = item.get(
                "priority",
                ActionItemPriority.MEDIUM,
            )

            assignee_name = item.get("assignee_name")
            assigned_to_user = None

            if assignee_name:
                member = WorkspaceMember.objects.filter(
                    workspace=meeting.workspace,
                    user__full_name__icontains=assignee_name
                ).first()
                
                if not member:
                     member = WorkspaceMember.objects.filter(
                        workspace=meeting.workspace,
                        user__first_name__icontains=assignee_name
                     ).first()

                if member:
                    assigned_to_user = member.user

            action_item = ActionItem.objects.create(
                meeting=meeting,
                title=item.get("title", ""),
                description=item.get(
                    "description",
                    "",
                ),
                priority=priority,
                assigned_to=assigned_to_user,
            )

            created_items.append(action_item)

        return created_items