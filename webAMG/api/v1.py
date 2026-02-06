"""
API v1 - Endpoints versionados para el sistema WebAMG.
Estas APIs siguen los estándares RESTful y las mejores prácticas de seguridad.
"""
import json
import logging
from typing import Optional, Dict, Any
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from webAMG.api import (
    api_endpoint,
    api_require_auth,
    api_require_admin,
    InputSanitizer,
    RateLimiter,
    APIResponse,
    validate_request_data,
    LoginRequest,
    CreateUserRequest,
    UpdateUserRequest,
    UnauthorizedError,
    BadRequestError,
    NotFoundError
)
from webAMG.services.auth_service import AuthService

logger = logging.getLogger(__name__)
User = get_user_model()


@api_endpoint(methods=['GET'], auth_required=False)
def health_check(request):
    """
    Endpoint de verificación de salud de la API v1.
    
    GET /api/v1/health/
    """
    return JsonResponse(APIResponse.success(
        data={
            'status': 'healthy',
            'version': '1.0.0',
            'service': 'WebAMG API v1'
        },
        message='API is running'
    ))


@api_endpoint(methods=['GET'], auth_required=False)
def api_info(request):
    """
    Endpoint con información sobre la API v1.
    
    GET /api/v1/info/
    """
    return JsonResponse(APIResponse.success(
        data={
            'name': 'WebAMG API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/v1/health/',
                'info': '/api/v1/info/',
                'auth': {
                    'login': '/api/v1/auth/login/',
                    'logout': '/api/v1/auth/logout/',
                    'verify': '/api/v1/auth/verify/',
                    'current_user': '/api/v1/auth/me/'
                },
                'users': {
                    'list': '/api/v1/users/',
                    'create': '/api/v1/users/',
                    'detail': '/api/v1/users/{id}/',
                    'update': '/api/v1/users/{id}/',
                    'delete': '/api/v1/users/{id}/'
                }
            }
        }
    ))


@api_endpoint(methods=['POST'], auth_required=False, csrf_exempt=True)
def login(request):
    """
    Endpoint de API para iniciar sesión con rate limiting.
    
    POST /api/v1/auth/login/
    
    Body:
        username: str (3-50 chars)
        password: str (min 6 chars)
    """
    try:
        data = json.loads(request.body)
        
        validated = validate_request_data(data, LoginRequest)
        
        ip_address = InputSanitizer.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        RateLimiter.check_rate_limit(
            f"login_{validated.username}",
            'login',
            limit=5,
            window=300
        )
        
        result = AuthService.login(
            validated.username,
            validated.password,
            ip_address,
            user_agent
        )
        
        if result['success']:
            response = JsonResponse(APIResponse.success(
                data={
                    'user': result['user'],
                    'expires_at': result['expires_at']
                },
                message='Login exitoso'
            ))
            
            response.set_cookie(
                'session_token',
                result['session_token'],
                max_age=8 * 60 * 60,
                httponly=True,
                samesite='Lax',
                secure=not request.META.get('HTTP_X_FORWARDED_PROTO') == 'http'
            )
            
            logger.info(f"User {validated.username} logged in from {ip_address}")
            
            return response
        else:
            logger.warning(f"Failed login attempt for {validated.username} from {ip_address}")
            raise UnauthorizedError(result['error'])
            
    except json.JSONDecodeError:
        raise BadRequestError('JSON inválido')
    except Exception as e:
        if not isinstance(e, (UnauthorizedError, BadRequestError)):
            logger.error(f"Unexpected error in login: {str(e)}")
            raise


@api_endpoint(methods=['POST'], auth_required=True)
def logout(request):
    """
    Endpoint de API para cerrar sesión.
    
    POST /api/v1/auth/logout/
    
    Headers:
        X-Session-Token: str (optional, falls back to cookie)
    
    Cookies:
        session_token: str
    """
    session_token = (
        request.COOKIES.get('session_token') or 
        request.headers.get('X-Session-Token')
    )
    
    if not session_token:
        raise BadRequestError('No hay sesión activa')
    
    result = AuthService.logout(session_token)
    
    if result['success']:
        response = JsonResponse(APIResponse.success(message='Logout exitoso'))
        response.delete_cookie('session_token')
        
        logger.info(f"User {request.user.username if hasattr(request, 'user') else 'unknown'} logged out")
        
        return response
    else:
        raise BadRequestError(result['error'])


@api_endpoint(methods=['GET'], auth_required=True)
def verify_session(request):
    """
    Endpoint de API para verificar la sesión actual.
    
    GET /api/v1/auth/verify/
    
    Headers:
        X-Session-Token: str (optional, falls back to cookie)
    """
    session_token = (
        request.COOKIES.get('session_token') or 
        request.headers.get('X-Session-Token')
    )
    
    if not session_token:
        raise UnauthorizedError('No hay sesión activa')
    
    result = AuthService.verify_session(session_token)
    
    if result.get('valid'):
        return JsonResponse(APIResponse.success(
            data={'user': result['user']},
            message='Sesión válida'
        ))
    else:
        raise UnauthorizedError(result.get('error', 'Sesión inválida'))


@api_endpoint(methods=['GET'], auth_required=True)
def current_user(request):
    """
    Endpoint de API para obtener el usuario actual.
    
    GET /api/v1/auth/me/
    """
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'full_name': request.user.full_name,
        'role': request.user.role,
        'profile_image_url': request.user.profile_image_url,
        'is_active': request.user.is_active,
        'last_login': request.user.last_login.isoformat() if request.user.last_login else None
    }
    
    return JsonResponse(APIResponse.success(data={'user': user_data}))


@api_endpoint(methods=['GET'], auth_required=True)
def list_users(request):
    """
    Endpoint para listar usuarios con paginación.
    
    GET /api/v1/users/
    
    Query params:
        page: int (default: 1)
        page_size: int (default: 20, max: 100)
        search: str (optional)
        role: str (optional: 'administrador', 'usuario')
        is_active: bool (optional)
    """
    from django.core.paginator import Paginator
    
    page = int(request.GET.get('page', 1))
    page_size = min(int(request.GET.get('page_size', 20)), 100)
    search = request.GET.get('search', '').strip()
    role = request.GET.get('role', '').strip()
    is_active = request.GET.get('is_active')
    
    queryset = User.objects.all()
    
    if search:
        queryset = queryset.filter(
            username__icontains=search
        ) | queryset.filter(
            email__icontains=search
        ) | queryset.filter(
            full_name__icontains=search
        )
    
    if role:
        queryset = queryset.filter(role=role)
    
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        queryset = queryset.filter(is_active=is_active_bool)
    
    queryset = queryset.order_by('-created_at')
    
    paginator = Paginator(queryset, page_size)
    users_page = paginator.get_page(page)
    
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        for user in users_page
    ]
    
    return JsonResponse(APIResponse.paginated(
        items=users_data,
        page=page,
        page_size=page_size,
        total=paginator.count,
        message=f'{len(users_data)} usuarios encontrados'
    ))


@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def create_user(request):
    """
    Endpoint para crear un nuevo usuario (solo administradores).
    
    POST /api/v1/users/
    
    Body:
        username: str (3-30 chars, alphanumeric, underscores, hyphens)
        email: str (valid email)
        password: str (min 8 chars, must contain uppercase, lowercase, and number)
        full_name: str (2-100 chars)
        role: str (default: 'usuario', options: 'administrador', 'usuario')
    """
    data = json.loads(request.body)
    validated = validate_request_data(data, CreateUserRequest)
    
    if User.objects.filter(username=validated.username).exists():
        from webAMG.api import ConflictError
        raise ConflictError('El nombre de usuario ya existe')
    
    if User.objects.filter(email=validated.email).exists():
        from webAMG.api import ConflictError
        raise ConflictError('El email ya está registrado')
    
    user = User.objects.create_user(
        username=validated.username,
        email=validated.email,
        password=validated.password,
        full_name=validated.full_name,
        role=validated.role,
        is_active=True
    )
    
    logger.info(f"User {validated.username} created by {request.user.username}")
    
    return JsonResponse(
        APIResponse.success(
            data={
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'is_active': user.is_active
                }
            },
            message='Usuario creado exitosamente'
        ),
        status=201
    )


@api_endpoint(methods=['GET'], auth_required=True)
def user_detail(request, user_id: int):
    """
    Endpoint para obtener detalles de un usuario específico.
    
    GET /api/v1/users/{id}/
    """
    user = User.objects.filter(id=user_id).first()
    
    if not user:
        from webAMG.api import NotFoundError
        raise NotFoundError('Usuario no encontrado')
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'last_login': user.last_login.isoformat() if user.last_login else None
    }
    
    return JsonResponse(APIResponse.success(data={'user': user_data}))


@api_endpoint(methods=['PUT', 'PATCH'], auth_required=True, roles={'administrador'})
def update_user(request, user_id: int):
    """
    Endpoint para actualizar un usuario (solo administradores).
    
    PUT /api/v1/users/{id}/ - Reemplaza todo el usuario
    PATCH /api/v1/users/{id}/ - Actualiza campos específicos
    
    Body (all optional for PATCH):
        email: str
        full_name: str
        role: str
        is_active: bool
    """
    user = User.objects.filter(id=user_id).first()
    
    if not user:
        from webAMG.api import NotFoundError
        raise NotFoundError('Usuario no encontrado')
    
    data = json.loads(request.body)
    validated = validate_request_data(data, UpdateUserRequest)
    
    if validated.email and User.objects.exclude(id=user_id).filter(email=validated.email).exists():
        from webAMG.api import ConflictError
        raise ConflictError('El email ya está registrado')
    
    if validated.email is not None:
        user.email = validated.email
    if validated.full_name is not None:
        user.full_name = validated.full_name
    if validated.role is not None:
        user.role = validated.role
    if validated.is_active is not None:
        user.is_active = validated.is_active
    
    user.save()
    
    logger.info(f"User {user_id} updated by {request.user.username}")
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'role': user.role,
        'is_active': user.is_active
    }
    
    return JsonResponse(APIResponse.success(
        data={'user': user_data},
        message='Usuario actualizado exitosamente'
    ))


@api_endpoint(methods=['DELETE'], auth_required=True, roles={'administrador'})
def delete_user(request, user_id: int):
    """
    Endpoint para eliminar un usuario (solo administradores).
    
    DELETE /api/v1/users/{id}/
    """
    if user_id == request.user.id:
        from webAMG.api import BadRequestError
        raise BadRequestError('No puedes eliminar tu propio usuario')
    
    user = User.objects.filter(id=user_id).first()
    
    if not user:
        from webAMG.api import NotFoundError
        raise NotFoundError('Usuario no encontrado')
    
    username = user.username
    user.delete()
    
    logger.info(f"User {username} (ID: {user_id}) deleted by {request.user.username}")
    
    return JsonResponse(
        APIResponse.success(message=f'Usuario {username} eliminado exitosamente')
    )


@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def deactivate_project(request, project_id):
    """
    Endpoint para desactivar (soft delete) un proyecto.
    
    POST /api/v1/projects/{id}/deactivate/
    
    Solo los administradores pueden desactivar proyectos.
    """
    from webAMG.models import Project
    
    project = Project.objects.filter(id=project_id).first()
    
    if not project:
        raise NotFoundError('Proyecto no encontrado')
    
    if not project.is_active:
        raise BadRequestError('El proyecto ya está inactivo')
    
    project.is_active = False
    project.save()
    
    logger.info(f"Project {project.project_name} (ID: {project_id}) deactivated by {request.user.username}")
    
    return JsonResponse(
        APIResponse.success(message='Proyecto desactivado exitosamente')
    )


@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def activate_project(request, project_id):
    """
    Endpoint para reactivar un proyecto.
    
    POST /api/v1/projects/{id}/activate/
    
    Solo los administradores pueden reactivar proyectos.
    """
    from webAMG.models import Project
    
    project = Project.objects.filter(id=project_id).first()
    
    if not project:
        raise NotFoundError('Proyecto no encontrado')
    
    if project.is_active:
        raise BadRequestError('El proyecto ya está activo')
    
    project.is_active = True
    project.save()
    
    logger.info(f"Project {project.project_name} (ID: {project_id}) activated by {request.user.username}")
    
    return JsonResponse(
        APIResponse.success(message='Proyecto reactivado exitosamente')
    )