"""
Domain errors and HTTP exception mapping.
"""

from typing import Optional
from fastapi import HTTPException, status


class DomainError(Exception):
    """Base class for domain errors."""

    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code or "DOMAIN_ERROR"
        super().__init__(message)


class NotFoundError(DomainError):
    """Resource not found error."""

    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found",
            code="NOT_FOUND",
        )


class ValidationError(DomainError):
    """Validation error for invalid data."""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message=message, code="VALIDATION_ERROR")


class ConflictError(DomainError):
    """Conflict error for duplicate resources."""

    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(
            message=f"{resource} with identifier '{identifier}' already exists",
            code="CONFLICT",
        )


class ServiceUnavailableError(DomainError):
    """External service unavailable."""

    def __init__(self, service: str, message: Optional[str] = None):
        self.service = service
        super().__init__(
            message=message or f"Service '{service}' is unavailable",
            code="SERVICE_UNAVAILABLE",
        )


def domain_error_to_http(error: DomainError) -> HTTPException:
    """
    Convert a domain error to an HTTP exception.

    Args:
        error: Domain error instance

    Returns:
        FastAPI HTTPException
    """
    if isinstance(error, NotFoundError):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": error.message, "code": error.code},
        )
    elif isinstance(error, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "message": error.message,
                "code": error.code,
                "field": error.field,
            },
        )
    elif isinstance(error, ConflictError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": error.message, "code": error.code},
        )
    elif isinstance(error, ServiceUnavailableError):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": error.message, "code": error.code},
        )
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": error.message, "code": error.code},
        )
