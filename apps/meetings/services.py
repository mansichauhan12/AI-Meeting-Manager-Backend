# from django.db import transaction

# from .constants import (
#     ALLOWED_AUDIO_EXTENSIONS,
#     MAX_AUDIO_FILE_SIZE,
# )
# from .exceptions import (
#     InvalidMeetingFileException,
#     MeetingAccessDeniedException,
# )
# from .models import Meeting
# from .choices import MeetingStatus


# class MeetingService:

#     @staticmethod
#     def validate_audio_file(audio_file):

#         if not audio_file:
#             raise InvalidMeetingFileException(
#                 "Audio file is required."
#             )

#         file_name = audio_file.name.lower()

#         if "." not in file_name:
#             raise InvalidMeetingFileException(
#                 "File must have a valid extension."
#             )

#         extension = "." + file_name.split(".")[-1]

#         if extension not in ALLOWED_AUDIO_EXTENSIONS:
#             raise InvalidMeetingFileException(
#                 "Unsupported audio format. "
#                 "Supported formats: MP3, WAV, M4A, MP4, WEBM."
#             )

#         if audio_file.size > MAX_AUDIO_FILE_SIZE:
#             raise InvalidMeetingFileException(
#                 "Audio file size cannot exceed 100 MB."
#             )

#         return True

#     @staticmethod
#     @transaction.atomic
#     def create_meeting(
#         *,
#         user,
#         workspace,
#         title,
#         meeting_date,
#         audio_file,
#     ):

#         MeetingService.validate_audio_file(
#             audio_file
#         )

#         meeting = Meeting.objects.create(
#             workspace=workspace,
#             title=title,
#             meeting_date=meeting_date,
#             audio_file=audio_file,
#             file_name=audio_file.name,
#             status=MeetingStatus.UPLOADED,
#             created_by=user,
#         )

#         return meeting

#     @staticmethod
#     def delete_meeting(
#         *,
#         user,
#         meeting,
#     ):

#         if meeting.created_by_id != user.id:
#             raise MeetingAccessDeniedException(
#                 "Only the meeting creator can delete this meeting."
#             )

#         meeting.delete()

from django.db import transaction

from apps.workspace.models import WorkspaceMember

from .choices import MeetingStatus
from .constants import (
    ALLOWED_AUDIO_EXTENSIONS,
    MAX_AUDIO_FILE_SIZE,
)
from .exceptions import (
    InvalidMeetingFileException,
    MeetingAccessDeniedException,
)
from .models import Meeting
from .tasks import process_meeting

class MeetingService:

    @staticmethod
    def validate_workspace_access(
        *,
        user,
        workspace_id,
    ):

        is_member = WorkspaceMember.objects.filter(
            workspace_id=workspace_id,
            user=user,
            status="ACTIVE",
        ).exists()

        if not is_member:
            raise MeetingAccessDeniedException(
                "You are not a member of this workspace."
            )

        return True

    @staticmethod
    def validate_audio_file(audio_file):

        if not audio_file:
            raise InvalidMeetingFileException(
                "Audio file is required."
            )

        file_name = audio_file.name.lower()

        if "." not in file_name:
            raise InvalidMeetingFileException(
                "File must have a valid extension."
            )

        extension = "." + file_name.split(".")[-1]

        if extension not in ALLOWED_AUDIO_EXTENSIONS:
            raise InvalidMeetingFileException(
                "Unsupported audio format. "
                "Supported formats: MP3, WAV, M4A, MP4, WEBM."
            )

        if audio_file.size > MAX_AUDIO_FILE_SIZE:
            raise InvalidMeetingFileException(
                "Audio file size cannot exceed 100 MB."
            )

        return True

    @staticmethod
    @transaction.atomic
    def create_meeting(
        *,
        user,
        workspace,
        title,
        meeting_date,
        audio_file,
    ):

        MeetingService.validate_workspace_access(
            user=user,
            workspace_id=workspace.id,
        )

        MeetingService.validate_audio_file(
            audio_file
        )

        meeting = Meeting.objects.create(
            workspace=workspace,
            title=title,
            meeting_date=meeting_date,
            audio_file=audio_file,
            file_name=audio_file.name,
            status=MeetingStatus.PROCESSING,
            created_by=user,
        )

        transaction.on_commit(
            lambda: process_meeting.delay(meeting.id)
        )

        return meeting



    @staticmethod
    def delete_meeting(
        *,
        user,
        meeting,
    ):

        if meeting.created_by_id != user.id:
            raise MeetingAccessDeniedException(
                "Only the meeting creator can delete this meeting."
            )

        meeting.delete()