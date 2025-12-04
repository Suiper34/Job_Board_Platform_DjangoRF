from __future__ import annotations

import logging
from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


class JobBoardError(Exception):
    """Base exception for the job board domain."""


class InvalidResumeException(JobBoardError):
    """Raised when resume parsing fails or file is invalid."""


class ApplicationWorkflowError(JobBoardError):
    """Raised when an invalid application status transition is attempted."""


def custom_exception_handler(
        e: Exception,
        context: dict[str, Any]
) -> Response | None:
    """
    Provide a consistent API error structure while delegating to DRF defaults
    when possible.
    """

    response = drf_exception_handler(e, context)

    if response is not None:
        return response

    logger.exception('Unhandled exception in API.',
                     exc_info=e, extra={'context': context})

    return Response(
        {'detail': 'An unexpected error occurred. Please try again later.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
