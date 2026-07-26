from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response | None:
    """Wrap every DRF error response in one consistent shape."""
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(response.data, dict) and "detail" in response.data and len(response.data) == 1:
        errors = None
        message = response.data["detail"]
    else:
        errors = response.data
        message = "Validation failed."

    response.data = {"success": False, "message": message, "errors": errors}
    return response
