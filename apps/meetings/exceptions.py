from rest_framework.exceptions import APIException


class MeetingNotFoundException(APIException):
    status_code = 404
    default_detail = "Meeting not found."
    default_code = "MEETING_NOT_FOUND"


class MeetingAccessDeniedException(APIException):
    status_code = 403
    default_detail = "You do not have access to this meeting."
    default_code = "MEETING_ACCESS_DENIED"


class InvalidMeetingFileException(APIException):
    status_code = 400
    default_detail = "Invalid meeting file."
    default_code = "INVALID_MEETING_FILE"