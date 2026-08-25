# from celery import shared_task

# from .models import Meeting


# @shared_task
# def process_meeting(meeting_id):

#     try:
#         meeting = Meeting.objects.get(
#             id=meeting_id
#         )

#         print(
#             f"Processing meeting: {meeting.id}"
#         )

#         # --------------------------------
#         # Future AI pipeline
#         # --------------------------------

#         # 1. Audio → Transcript
#         # 2. Transcript → Summary
#         # 3. Transcript → Action Items
#         # 4. Transcript → Embeddings

#         # Temporary simulation
#         meeting.status = "COMPLETED"

#         meeting.save(
#             update_fields=["status"]
#         )

#         return {
#             "meeting_id": meeting.id,
#             "status": "COMPLETED",
#         }

#     except Meeting.DoesNotExist:

#         return {
#             "meeting_id": meeting_id,
#             "status": "FAILED",
#             "error": "Meeting not found",
#         }

#     except Exception as exc:

#         print(
#             f"Meeting processing failed: {exc}"
#         )

#         Meeting.objects.filter(
#             id=meeting_id
#         ).update(
#             status="FAILED"
#         )

#         raise


from celery import shared_task

from .choices import MeetingStatus
from .models import Meeting

from .services.transcription import (
    TranscriptionService,
)

from .services.summarization import (
    SummarizationService,
)

from .services.action_items import (
    ActionItemService,
)

from .services.action_item_persistence import (
    ActionItemPersistenceService,
)


@shared_task(
    bind=True,
    max_retries=3,
)
def process_meeting(self, meeting_id):

    try:

        meeting = Meeting.objects.get(
            id=meeting_id
        )

        meeting.status = MeetingStatus.PROCESSING

        meeting.error_message = ""

        meeting.save(
            update_fields=[
                "status",
                "error_message",
                "updated_at",
            ]
        )

        # --------------------------------
        # STEP 1: TRANSCRIPTION
        # --------------------------------

        transcript = (
            TranscriptionService.transcribe(
                meeting.audio_file.path
            )
        )

        meeting.transcript = transcript

        meeting.save(
            update_fields=[
                "transcript",
                "updated_at",
            ]
        )

        # --------------------------------
        # STEP 2: SUMMARY
        # --------------------------------

        summary = (
            SummarizationService.generate_summary(
                transcript
            )
        )

        meeting.summary = summary

        meeting.save(
            update_fields=[
                "summary",
                "updated_at",
            ]
        )

        # --------------------------------
        # STEP 3: ACTION ITEMS
        # --------------------------------

        result = (
            ActionItemService.extract_action_items(
                transcript
            )
        )

        action_items = result.get(
            "action_items",
            []
        )

        ActionItemPersistenceService.create_action_items(
            meeting=meeting,
            action_items=action_items,
        )

        # --------------------------------
        # STEP 4: COMPLETED
        # --------------------------------

        meeting.status = MeetingStatus.COMPLETED

        meeting.error_message = ""

        meeting.save(
            update_fields=[
                "status",
                "error_message",
                "updated_at",
            ]
        )

        return {
            "meeting_id": meeting.id,
            "status": MeetingStatus.COMPLETED,
        }

    except Meeting.DoesNotExist:

        return {
            "meeting_id": meeting_id,
            "status": MeetingStatus.FAILED,
        }

    except Exception as exc:

        Meeting.objects.filter(
            id=meeting_id
        ).update(
            status=MeetingStatus.FAILED,
            error_message=str(exc),
        )

        raise self.retry(
            exc=exc,
            countdown=60,
        )


from django.utils import timezone
from django.core.mail import send_mail
from .models import Reminder
from .choices import ReminderStatus

@shared_task
def check_pending_reminders():
    now = timezone.now()
    pending_reminders = Reminder.objects.filter(
        status=ReminderStatus.PENDING,
        send_at__lte=now
    )

    for reminder in pending_reminders:
        send_reminder_email.delay(reminder.id)

    return f"Enqueued {pending_reminders.count()} reminders."


@shared_task
def send_reminder_email(reminder_id):
    try:
        reminder = Reminder.objects.select_related("task", "task__assigned_to", "task__meeting").get(id=reminder_id)
        
        if reminder.status != ReminderStatus.PENDING:
            return "Reminder already processed."

        task = reminder.task
        user = task.assigned_to
        meeting = task.meeting

        if not user or not user.email:
            reminder.status = ReminderStatus.FAILED
            reminder.save(update_fields=["status"])
            return "No user email."

        subject = f"Reminder: {task.title}"
        
        body = (
            f"Hi {user.full_name or user.email},\n\n"
            f"This is a reminder for your action item:\n\n"
            f"Task:\n{task.title}\n\n"
            f"Meeting:\n{meeting.title}\n\n"
            f"Priority:\n{task.priority}\n\n"
        )
        
        if task.deadline:
            body += f"Deadline:\n{task.deadline.strftime('%B %d, %Y at %I:%M %p')}\n\n"
            
        body += (
            f"Please complete the task before the deadline.\n\n"
            f"AI Meeting Manager"
        )

        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False,
        )

        reminder.status = ReminderStatus.SENT
        reminder.save(update_fields=["status"])
        return f"Sent reminder to {user.email}"

    except Reminder.DoesNotExist:
        return "Reminder not found."
    except Exception as exc:
        Reminder.objects.filter(id=reminder_id).update(status=ReminderStatus.FAILED)
        return f"Failed to send email: {str(exc)}"