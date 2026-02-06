"""
Middleware para seguridad, zona horaria y logging de requests.
"""
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.http import JsonResponse
import logging
import time
from webAMG.api.security import SecurityHeaders


logger = logging.getLogger(__name__)


class TimezoneMiddleware(MiddlewareMixin):
    """
    Middleware para establecer la zona horaria de Guatemala en PostgreSQL y Django.
    """
    
    def process_request(self, request):
        """
        Establecer la zona horaria para la conexión actual a la base de datos y Django.
        """
        from django.db import connections
        
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SET TIME ZONE 'America/Guatemala'")
        except Exception as e:
            print(f'Error estableciendo zona horaria en PostgreSQL: {e}')
        
        try:
            timezone.activate('America/Guatemala')
        except Exception as e:
            print(f'Error activando zona horaria en Django: {e}')
        
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para agregar headers de seguridad HTTP a todas las respuestas.
    """
    
    def process_response(self, request, response):
        """
        Aplica headers de seguridad a la respuesta.
        """
        SecurityHeaders.apply_headers(response)
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para logging de requests con información de seguridad.
    """
    
    def process_request(self, request):
        """
        Registra el inicio de cada request.
        """
        request.start_time = time.time()
        
        return None
    
    def process_response(self, request, response):
        """
        Registra el final de cada request con métricas.
        """
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'ip': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
            }
            
            if hasattr(request, 'user') and request.user.is_authenticated:
                log_data['user_id'] = request.user.id
                log_data['username'] = request.user.username
            
            if response.status_code >= 400:
                logger.warning(f"Request with error: {log_data}")
            else:
                logger.info(f"Request: {log_data}")
        
        return response
    
    @staticmethod
    def _get_client_ip(request) -> str:
        """
        Obtiene la dirección IP del cliente de forma segura.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
