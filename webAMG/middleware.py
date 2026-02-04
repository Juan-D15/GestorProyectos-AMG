"""
Middleware para establecer la zona horaria en cada conexión a la base de datos.
Asegura que PostgreSQL y Django usen la zona horaria de Guatemala.
"""
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


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
                # Establecer la zona horaria para la sesión actual de PostgreSQL
                cursor.execute("SET TIME ZONE 'America/Guatemala'")
        except Exception as e:
            # Si falla, continuar sin interrumpir la aplicación
            print(f'Error estableciendo zona horaria en PostgreSQL: {e}')
        
        # Activar la zona horaria de Django
        try:
            timezone.activate('America/Guatemala')
            print(f'TimezoneMiddleware: Zona horaria activada: {timezone.get_current_timezone()}')
        except Exception as e:
            print(f'Error activando zona horaria en Django: {e}')
        
        return None
