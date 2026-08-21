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