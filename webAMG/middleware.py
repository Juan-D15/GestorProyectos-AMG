"""
Middleware para establecer la zona horaria en cada conexión a la base de datos.
Asegura que PostgreSQL use la zona horaria de Guatemala.
"""
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    """
    Middleware para establecer la zona horaria de Guatemala en PostgreSQL.
    """
    
    def process_request(self, request):
        """
        Establecer la zona horaria para la conexión actual a la base de datos.
        """
        from django.db import connections
        
        try:
            with connections['default'].cursor() as cursor:
                # Establecer la zona horaria para la sesión actual
                cursor.execute("SET TIME ZONE 'America/Guatemala'")
        except Exception:
            # Si falla, continuar sin interrumpir la aplicación
            pass
        
        return None
