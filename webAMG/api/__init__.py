"""
Módulo API para endpoints de la aplicación.
Proporciona seguridad, validación y decoradores para APIs REST.
"""

from webAMG.api.exceptions import (
    APIError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ValidationError,
    RateLimitExceededError,
    InternalServerError,
    ServiceUnavailableError
)

from webAMG.api.decorators import (
    api_require_auth,
    api_require_roles,
    api_require_admin,
    api_require_methods,
    api_csrf_exempt,
    handle_api_errors,
    api_endpoint
)

from webAMG.api.security import (
    InputSanitizer,
    RateLimiter,
    SecurityHeaders,
    get_client_ip,
    get_request_fingerprint
)

from webAMG.api.validators import (
    BaseRequestModel,
    LoginRequest,
    CreateUserRequest,
    UpdateUserRequest,
    ProjectCreateRequest,
    ProjectUpdateRequest,
    BeneficiaryCreateRequest,
    BaseResponseModel,
    ErrorResponseModel,
    SuccessResponseModel,
    PaginatedResponseModel,
    APIResponse,
    validate_request_data
)

__all__ = [
    # Exceptions
    'APIError',
    'BadRequestError',
    'UnauthorizedError',
    'ForbiddenError',
    'NotFoundError',
    'ConflictError',
    'ValidationError',
    'RateLimitExceededError',
    'InternalServerError',
    'ServiceUnavailableError',
    # Decorators
    'api_require_auth',
    'api_require_roles',
    'api_require_admin',
    'api_require_methods',
    'api_csrf_exempt',
    'handle_api_errors',
    'api_endpoint',
    # Security
    'InputSanitizer',
    'RateLimiter',
    'SecurityHeaders',
    'get_client_ip',
    'get_request_fingerprint',
    # Validators
    'BaseRequestModel',
    'LoginRequest',
    'CreateUserRequest',
    'UpdateUserRequest',
    'ProjectCreateRequest',
    'ProjectUpdateRequest',
    'BeneficiaryCreateRequest',
    'BaseResponseModel',
    'ErrorResponseModel',
    'SuccessResponseModel',
    'PaginatedResponseModel',
    'APIResponse',
    'validate_request_data'
]
