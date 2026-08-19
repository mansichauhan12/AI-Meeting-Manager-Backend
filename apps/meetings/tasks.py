from celery import shared_task

from .models import Meeting


@shared_task
def process_meeting(meeting_id):

    try:
        meeting = Meeting.objects.get(
            id=meeting_id
        )

        print(
            f"Processing meeting: {meeting.id}"
        )

        # --------------------------------
        # Future AI pipeline
        # --------------------------------

        # 1. Audio → Transcript
        # 2. Transcript → Summary
        # 3. Transcript → Action Items
        # 4. Transcript → Embeddings

        # Temporary simulation
        meeting.status = "COMPLETED"

        meeting.save(
            update_fields=["status"]
        )

        return {
            "meeting_id": meeting.id,
            "status": "COMPLETED",
        }

    except Meeting.DoesNotExist:

        return {
            "meeting_id": meeting_id,
            "status": "FAILED",
            "error": "Meeting not found",
        }

    except Exception as exc:

        print(
            f"Meeting processing failed: {exc}"
        )

        Meeting.objects.filter(
            id=meeting_id
        ).update(
            status="FAILED"
        )

        raise