# Without this file, different kinds of errors (bad input, not logged in,
# not found) would each come back in a slightly different JSON shape. This
# rewrites every error into the same shape, so client code only has to
# handle one format, no matter what went wrong.

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response | None:
    """Wrap every DRF error response in one consistent shape."""
    response = exception_handler(exc, context)  # DRF's normal error handling
    if response is None:
        return None  # something DRF doesn't know how to handle - let Django deal with it

    # Simple errors (like "not logged in") come back as {"detail": "..."}.
    # Validation errors come back as {"field_name": ["what's wrong"]}.
    # Both get flattened into the same {success, message, errors} shape.
    if isinstance(response.data, dict) and "detail" in response.data and len(response.data) == 1:
        errors = None
        message = response.data["detail"]
    else:
        errors = response.data
        message = "Validation failed."

    response.data = {"success": False, "message": message, "errors": errors}
    return response
