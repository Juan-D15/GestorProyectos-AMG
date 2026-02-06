"""
Decoradores para las APIs del sistema WebAMG.
Proveen autenticación, autorización, rate limiting y validación de seguridad.
"""
import functools
from typing import Callable, Optional, List, Set
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from webAMG.api.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    RateLimitExceededError,
    BadRequestError
)
from webAMG.services.auth_service import AuthService


def api_require_auth(f: Optional[Callable] = None) -> Callable:
    """
    Decorador que requiere autenticación válida para acceder al endpoint.
    Valida el token de sesión desde cookie o header X-Session-Token.
    
    Args:
        f: Función a decorar
    
    Returns:
        Función decorada con validación de autenticación
    
    Raises:
        UnauthorizedError: Si no hay token o es inválido
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            session_token = (
                request.COOKIES.get('session_token') or 
                request.headers.get('X-Session-Token')
            )
            
            if not session_token:
                raise UnauthorizedError(
                    "Se requiere autenticación",
                    error_code="AUTH_REQUIRED"
                )
            
            result = AuthService.verify_session(session_token)
            
            if not result.get('valid'):
                raise UnauthorizedError(
                    result.get('error', 'Sesión inválida'),
                    error_code="INVALID_SESSION"
                )
            
            request.user_data = result['user']
            request.user = AuthService.get_user_from_session(session_token)
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    if f is None:
        return decorator
    else:
        return decorator(f)


def api_require_roles(roles: Set[str]) -> Callable:
    """
    Decorador que requiere que el usuario tenga roles específicos.
    Debe usarse junto con @api_require_auth.
    
    Args:
        roles: Conjunto de roles permitidos (ej: {'administrador', 'usuario'})
    
    Returns:
        Función decorada con validación de roles
    
    Raises:
        ForbiddenError: Si el usuario no tiene el rol requerido
    
    Example:
        @api_require_auth
        @api_require_roles({'administrador'})
        def admin_endpoint(request):
            return JsonResponse({'success': True})
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'user') or not request.user:
                raise ForbiddenError(
                    "Usuario no autenticado",
                    error_code="NOT_AUTHENTICATED"
                )
            
            user_role = getattr(request.user, 'role', None)
            
            if user_role not in roles:
                raise ForbiddenError(
                    f"Se requiere rol: {', '.join(roles)}",
                    error_code="INSUFFICIENT_PERMISSIONS",
                    details={'required_roles': list(roles), 'user_role': user_role}
                )
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator


def api_require_admin(f: Optional[Callable] = None) -> Callable:
    """
    Decorador que requiere rol de administrador.
    Combinación de @api_require_auth y @api_require_roles({'administrador'}).
    
    Args:
        f: Función a decorar
    
    Returns:
        Función decorada con validación de administrador
    
    Example:
        @api_require_admin
        def sensitive_operation(request):
            return JsonResponse({'success': True})
    """
    def decorator(view_func):
        return api_require_auth(
            api_require_roles({'administrador'})(view_func)
        )
    
    if f is None:
        return decorator
    else:
        return decorator(f)


def api_require_methods(methods: List[str]) -> Callable:
    """
    Decorador que restringe los métodos HTTP permitidos.
    Envuelve require_http_methods de Django con manejo de errores de API.
    
    Args:
        methods: Lista de métodos HTTP permitidos (ej: ['GET', 'POST'])
    
    Returns:
        Función decorada con restricción de métodos
    
    Raises:
        BadRequestError: Si el método no está permitido
    
    Example:
        @api_require_methods(['GET', 'POST'])
        def endpoint(request):
            return JsonResponse({'success': True})
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        @require_http_methods(methods)
        def wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    return decorator


def api_csrf_exempt(f: Callable) -> Callable:
    """
    Decorador que exime al endpoint de la protección CSRF.
    Útil para endpoints públicos de API (login, register, etc.).
    
    Args:
        f: Función a decorar
    
    Returns:
        Función decorada sin CSRF
    
    Example:
        @api_csrf_exempt
        @api_require_methods(['POST'])
        def public_api(request):
            return JsonResponse({'success': True})
    """
    return csrf_exempt(f)


def handle_api_errors(f: Callable) -> Callable:
    """
    Decorador que maneja excepciones de API y devuelve respuestas consistentes.
    Debe ser el último decorador aplicado (el más externo).
    
    Args:
        f: Función a decorar
    
    Returns:
        Función decorada con manejo de errores
    
    Example:
        @handle_api_errors
        @api_require_auth
        def endpoint(request):
            raise NotFoundError("Recurso no encontrado")
    """
    @functools.wraps(f)
    def wrapped_view(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except Exception as e:
            from webAMG.api.exceptions import APIError
            
            if isinstance(e, APIError):
                return JsonResponse(
                    e.to_dict(),
                    status=e.status_code
                )
            
            from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
            from django.http import Http404 as DjangoHttp404
            
            if isinstance(e, DjangoPermissionDenied):
                error = ForbiddenError(
                    "Permiso denegado",
                    error_code="PERMISSION_DENIED"
                )
                return JsonResponse(error.to_dict(), status=error.status_code)
            
            if isinstance(e, DjangoHttp404):
                error = NotFoundError(
                    "Recurso no encontrado",
                    error_code="NOT_FOUND"
                )
                return JsonResponse(error.to_dict(), status=error.status_code)
            
            from webAMG.api.exceptions import InternalServerError
            from django.conf import settings
            
            error = InternalServerError(
                "Error interno del servidor",
                details={'error': str(e)} if settings.DEBUG else None
            )
            return JsonResponse(error.to_dict(), status=error.status_code)
    
    return wrapped_view


def api_endpoint(
    methods: Optional[List[str]] = None,
    auth_required: bool = False,
    roles: Optional[Set[str]] = None,
    csrf_exempt: bool = False
) -> Callable:
    """
    Decorador combinado para endpoints de API.
    Simplifica la aplicación de múltiples decoradores.
    
    Args:
        methods: Lista de métodos HTTP permitidos
        auth_required: Si se requiere autenticación
        roles: Conjunto de roles permitidos (requiere auth_required=True)
        csrf_exempt: Si eximir de CSRF
    
    Returns:
        Función decorada con todas las configuraciones
    
    Example:
        @api_endpoint(methods=['GET'], auth_required=True)
        def protected_get(request):
            return JsonResponse({'success': True})
        
        @api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
        def admin_post(request):
            return JsonResponse({'success': True})
    """
    def decorator(view_func):
        decorated = view_func
        
        if csrf_exempt:
            decorated = api_csrf_exempt(decorated)
        
        if methods:
            decorated = api_require_methods(methods)(decorated)
        
        if auth_required:
            decorated = api_require_auth(decorated)
        
        if roles:
            decorated = api_require_roles(roles)(decorated)
        
        decorated = handle_api_errors(decorated)
        
        return decorated
    
    return decorator
