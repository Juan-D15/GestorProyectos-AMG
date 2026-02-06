"""
Excepciones personalizadas para las APIs del sistema WebAMG.
Proporcionan errores estructurados y consistentes para respuestas HTTP.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass


class APIError(Exception):
    """
    Base exception para todas las excepciones de API.
    Proporciona una estructura consistente para respuestas de error.
    """
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred"
    details: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        message: str,
        status_code: int = None,
        error_code: str = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.details = details
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la excepción a un diccionario para la respuesta JSON.
        """
        response = {
            'success': False,
            'error': self.error_code,
            'message': self.message
        }
        if self.details:
            response['details'] = self.details
        return response


class BadRequestError(APIError):
    """Error 400 Bad Request."""
    status_code = 400
    error_code = "BAD_REQUEST"


class UnauthorizedError(APIError):
    """Error 401 Unauthorized."""
    status_code = 401
    error_code = "UNAUTHORIZED"


class ForbiddenError(APIError):
    """Error 403 Forbidden."""
    status_code = 403
    error_code = "FORBIDDEN"


class NotFoundError(APIError):
    """Error 404 Not Found."""
    status_code = 404
    error_code = "NOT_FOUND"


class ConflictError(APIError):
    """Error 409 Conflict."""
    status_code = 409
    error_code = "CONFLICT"


class ValidationError(APIError):
    """Error 422 Unprocessable Entity - Validación fallida."""
    status_code = 422
    error_code = "VALIDATION_ERROR"


class RateLimitExceededError(APIError):
    """Error 429 Too Many Requests."""
    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"


class InternalServerError(APIError):
    """Error 500 Internal Server Error."""
    status_code = 500
    error_code = "INTERNAL_ERROR"


class ServiceUnavailableError(APIError):
    """Error 503 Service Unavailable."""
    status_code = 503
    error_code = "SERVICE_UNAVAILABLE"
