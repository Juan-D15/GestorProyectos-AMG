"""
Vistas para APIs y endpoints de la aplicación.
Este módulo contiene todas las vistas que devuelven JSON o manejan datos.
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from webAMG.services.auth_service import AuthService


@require_http_methods(["GET"])
def health_check(request):
    """
    Endpoint de verificación de salud de la API.
    Retorna el estado del servidor.
    """
    return JsonResponse({
        "status": "healthy",
        "message": "API is running",
        "service": "WebAMG API"
    })


@require_http_methods(["GET"])
def api_info(request):
    """
    Endpoint con información sobre la API.
    """
    return JsonResponse({
        "name": "WebAMG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health/",
            "info": "/api/info/",
            "auth": {
                "login": "/api/auth/login/",
                "logout": "/api/auth/logout/",
                "verify": "/api/auth/verify/",
            }
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def example_api(request):
    """
    Ejemplo de endpoint API que recibe datos JSON.
    """
    try:
        data = json.loads(request.body)
        return JsonResponse({
            "success": True,
            "message": "Data received successfully",
            "data": data
        })
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data"
        }, status=400)


# =====================================================
# VISTAS DE AUTENTICACIÓN (API)
# =====================================================

@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """
    Endpoint de API para iniciar sesión.
    
    Body JSON:
        username: Nombre de usuario
        password: Contraseña
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Se requieren username y password'
            }, status=400)
        
        # Obtener IP y User Agent
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Intentar login
        result = AuthService.login(username, password, ip_address, user_agent)
        
        if result['success']:
            response = JsonResponse({
                'success': True,
                'message': 'Login exitoso',
                'user': result['user'],
                'expires_at': result['expires_at']
            })
            
            # Establecer cookie con el token de sesión
            response.set_cookie(
                'session_token',
                result['session_token'],
                max_age=8 * 60 * 60,  # 8 horas
                httponly=True,
                samesite='Lax'
            )
            
            return response
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
def api_logout(request):
    """
    Endpoint de API para cerrar sesión.
    """
    # Obtener token de sesión
    session_token = request.COOKIES.get('session_token') or request.headers.get('X-Session-Token')
    
    if not session_token:
        return JsonResponse({
            'success': False,
            'error': 'No hay sesión activa'
        }, status=400)
    
    # Cerrar sesión
    result = AuthService.logout(session_token)
    
    if result['success']:
        response = JsonResponse({
            'success': True,
            'message': 'Logout exitoso'
        })
        
        # Eliminar cookie
        response.delete_cookie('session_token')
        
        return response
    else:
        return JsonResponse({
            'success': False,
            'error': result['error']
        }, status=400)


@require_http_methods(["GET"])
def api_verify_session(request):
    """
    Endpoint de API para verificar la sesión actual.
    """
    # Obtener token de sesión
    session_token = request.COOKIES.get('session_token') or request.headers.get('X-Session-Token')
    
    if not session_token:
        return JsonResponse({
            'valid': False,
            'error': 'No hay sesión activa'
        })
    
    # Verificar sesión
    result = AuthService.verify_session(session_token)
    
    return JsonResponse(result)


@require_http_methods(["GET"])
def api_current_user(request):
    """
    Endpoint de API para obtener el usuario actual.
    """
    # Verificar si hay usuario en el request (del middleware)
    if hasattr(request, 'user_data'):
        return JsonResponse({
            'success': True,
            'user': request.user_data
        })
    else:
        # Verificar sesión manualmente
        session_token = request.COOKIES.get('session_token') or request.headers.get('X-Session-Token')
        
        if not session_token:
            return JsonResponse({
                'success': False,
                'error': 'No autenticado'
            }, status=401)
        
        result = AuthService.verify_session(session_token)
        
        if result['valid']:
            return JsonResponse({
                'success': True,
                'user': result['user']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=401)


# =====================================================
# UTILIDADES
# =====================================================

def get_client_ip(request):
    """
    Obtiene la dirección IP del cliente.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
