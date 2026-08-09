from rest_framework.exceptions import APIException


class WorkspaceException(APIException):

    status_code = 400

    default_detail = "Workspace Error"

    default_code = "workspace_error"


class WorkspaceNotFound(WorkspaceException):

    status_code = 404

    default_detail = "Workspace not found"


class WorkspacePermissionDenied(WorkspaceException):

    status_code = 403

    default_detail = "Permission denied"


class MemberAlreadyExists(WorkspaceException):

    default_detail = "Member already exists"


class MemberNotFound(WorkspaceException):

    status_code = 404

    default_detail = "Member not found"