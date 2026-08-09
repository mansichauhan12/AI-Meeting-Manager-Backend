from django.db import models


class WorkspaceRole(models.TextChoices):

    OWNER = "OWNER", "Owner"

    ADMIN = "ADMIN", "Admin"

    MEMBER = "MEMBER", "Member"


class WorkspaceMemberStatus(models.TextChoices):

    INVITED = "INVITED", "Invited"

    ACTIVE = "ACTIVE", "Active"

    REMOVED = "REMOVED", "Removed"