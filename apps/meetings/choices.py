from django.db import models


class MeetingStatus(models.TextChoices):

    UPLOADED = "UPLOADED", "Uploaded"

    PROCESSING = "PROCESSING", "Processing"

    COMPLETED = "COMPLETED", "Completed"

    FAILED = "FAILED", "Failed"


class ActionItemStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    IN_PROGRESS = "IN_PROGRESS", "In Progress"

    DONE = "DONE", "Done"


class ActionItemPriority(models.TextChoices):

    LOW = "LOW", "Low"

    MEDIUM = "MEDIUM", "Medium"

    HIGH = "HIGH", "High"

    URGENT = "URGENT", "Urgent"


class ReminderStatus(models.TextChoices):

    PENDING = "PENDING", "Pending"

    SENT = "SENT", "Sent"

    FAILED = "FAILED", "Failed"