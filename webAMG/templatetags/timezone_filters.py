"""
Template filters para manejo de fechas con zona horaria.
"""
from django import template
from django.utils import timezone
from datetime import timezone as dt_timezone

register = template.Library()


@register.filter
def localtime_filter(value):
    """
    Convierte un datetime a la zona horaria local.
    """
    if value is None:
        return value
    
    try:
        # Primero asegurar que el valor esté en UTC
        if value.tzinfo is None:
            value = value.replace(tzinfo=dt_timezone.utc)
        
        # Convertir a la zona horaria local
        local_time = timezone.localtime(value)
        print(f'localtime_filter: {value} -> {local_time} (tz: {local_time.tzinfo})')
        return local_time
    except Exception as e:
        print(f'Error en localtime_filter: {e}')
        return value
