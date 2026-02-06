"""
Módulo de seguridad para las APIs del sistema WebAMG.
Proporciona funciones para sanitización, validación y rate limiting.
"""
import re
import hashlib
import secrets
from typing import Optional, List, Dict, Any
from django.core.cache import cache
from django.conf import settings
from webAMG.api.exceptions import BadRequestError, RateLimitExceededError


class InputSanitizer:
    """
    Clase para sanitizar y validar inputs de usuario.
    Previene ataques como XSS, SQL Injection, etc.
    """
    
    XSS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>',
        r'<embed[^>]*>.*?</embed>',
    ]
    
    SQL_INJECTION_PATTERNS = [
        r"(\bor\b|\band\b)\s+\w+\s*=",
        r";\s*drop\b",
        r";\s*delete\b",
        r";\s*insert\b",
        r";\s*update\b",
        r"union\s+select",
        r"'\s*or\s*'",
        r'"\s*or\s*"',
        r"'\s*--",
        r'"\s*--',
    ]
    
    @staticmethod
    def sanitize_string(value: str, allow_html: bool = False) -> str:
        """
        Sanitiza una cadena de texto para prevenir XSS y SQL Injection.
        
        Args:
            value: Cadena a sanitizar
            allow_html: Si se permite HTML (usar con precaución)
        
        Returns:
            Cadena sanitizada
        """
        if not isinstance(value, str):
            return str(value)
        
        if not allow_html:
            for pattern in InputSanitizer.XSS_PATTERNS:
                value = re.sub(pattern, '', value, flags=re.IGNORECASE)
        
        for pattern in InputSanitizer.SQL_INJECTION_PATTERNS:
            if re.search(pattern, value, flags=re.IGNORECASE):
                raise BadRequestError(
                    "Input contains potentially malicious content",
                    error_code="MALICIOUS_INPUT"
                )
        
        return value.strip()
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Valida y sanitiza un email.
        
        Args:
            email: Email a validar
        
        Returns:
            Email en minúsculas y sanitizado
        
        Raises:
            BadRequestError: Si el email no es válido
        """
        email = email.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise BadRequestError(
                "Email inválido",
                error_code="INVALID_EMAIL"
            )
        
        return email
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        """
        Valida y sanitiza un nombre de usuario.
        Solo permite letras, números, guiones y guiones bajos.
        
        Args:
            username: Nombre de usuario a validar
        
        Returns:
            Nombre de usuario sanitizado
        
        Raises:
            BadRequestError: Si el nombre de usuario no es válido
        """
        username = username.strip().lower()
        username_pattern = r'^[a-zA-Z0-9_-]{3,30}$'
        
        if not re.match(username_pattern, username):
            raise BadRequestError(
                "Nombre de usuario inválido. Debe tener 3-30 caracteres y solo puede contener letras, números, guiones y guiones bajos",
                error_code="INVALID_USERNAME"
            )
        
        return username
    
    @staticmethod
    def sanitize_phone(phone: str) -> str:
        """
        Valida y sanitiza un número de teléfono.
        Solo permite dígitos y formatos de Guatemala (+502, Guatemala).
        
        Args:
            phone: Número de teléfono a validar
        
        Returns:
            Número de teléfono formateado
        
        Raises:
            BadRequestError: Si el número de teléfono no es válido
        """
        phone = re.sub(r'[^\d+]', '', phone)
        guatemala_pattern = r'^(\+502)?[2-9]\d{7}$'
        
        if not re.match(guatemala_pattern, phone):
            raise BadRequestError(
                "Número de teléfono inválido. Formato válido: +502XXXXXXX o XXXXXXXX",
                error_code="INVALID_PHONE"
            )
        
        return phone
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], fields: Dict[str, str]) -> Dict[str, Any]:
        """
        Sanitiza un diccionario de datos basándose en reglas de campo.
        
        Args:
            data: Diccionario a sanitizar
            fields: Diccionario con reglas de sanitización por campo
                   {'field_name': 'sanitizer_type'}
        
        Returns:
            Diccionario sanitizado
        
        Example:
            data = {'username': 'john', 'email': 'john@example.com'}
            fields = {'username': 'username', 'email': 'email'}
            result = InputSanitizer.sanitize_dict(data, fields)
        """
        sanitized = {}
        
        for field, sanitizer_type in fields.items():
            if field not in data:
                continue
            
            value = data[field]
            
            if value is None:
                sanitized[field] = None
                continue
            
            try:
                if sanitizer_type == 'string':
                    sanitized[field] = InputSanitizer.sanitize_string(value)
                elif sanitizer_type == 'email':
                    sanitized[field] = InputSanitizer.sanitize_email(value)
                elif sanitizer_type == 'username':
                    sanitized[field] = InputSanitizer.sanitize_username(value)
                elif sanitizer_type == 'phone':
                    sanitized[field] = InputSanitizer.sanitize_phone(value)
                else:
                    sanitized[field] = value
            except BadRequestError as e:
                e.details = e.details or {}
                e.details['field'] = field
                raise
        
        return sanitized


class RateLimiter:
    """
    Clase para implementar rate limiting en endpoints de API.
    Usa Django cache para almacenar contadores.
    """
    
    @staticmethod
    def _get_key(
        identifier: str,
        endpoint: str,
        window: int
    ) -> str:
        """
        Genera una clave única para el rate limiter.
        
        Args:
            identifier: Identificador único (IP, user_id, etc.)
            endpoint: Nombre del endpoint
            window: Ventana de tiempo en segundos
        
        Returns:
            Clave de cache
        """
        key_data = f"{identifier}:{endpoint}:{window}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    @staticmethod
    def is_rate_limited(
        identifier: str,
        endpoint: str,
        limit: int,
        window: int = 60
    ) -> bool:
        """
        Verifica si un identificador ha excedido el límite de solicitudes.
        
        Args:
            identifier: Identificador único (IP, user_id, etc.)
            endpoint: Nombre del endpoint
            limit: Número máximo de solicitudes permitidas
            window: Ventana de tiempo en segundos (default: 60)
        
        Returns:
            True si está rate limited, False si puede continuar
        """
        key = RateLimiter._get_key(identifier, endpoint, window)
        
        try:
            current = cache.get(key, 0)
            
            if current >= limit:
                return True
            
            cache.set(key, current + 1, timeout=window)
            return False
            
        except Exception:
            return False
    
    @staticmethod
    def check_rate_limit(
        identifier: str,
        endpoint: str,
        limit: int,
        window: int = 60
    ) -> None:
        """
        Verifica y lanza excepción si está rate limited.
        
        Args:
            identifier: Identificador único (IP, user_id, etc.)
            endpoint: Nombre del endpoint
            limit: Número máximo de solicitudes permitidas
            window: Ventana de tiempo en segundos (default: 60)
        
        Raises:
            RateLimitExceededError: Si ha excedido el límite
        """
        if RateLimiter.is_rate_limited(identifier, endpoint, limit, window):
            raise RateLimitExceededError(
                f"Demasiadas solicitudes. Límite: {limit} por {window} segundos",
                error_code="RATE_LIMIT_EXCEEDED",
                details={
                    'limit': limit,
                    'window': window,
                    'retry_after': window
                }
            )
    
    @staticmethod
    def get_remaining_requests(
        identifier: str,
        endpoint: str,
        limit: int,
        window: int = 60
    ) -> Dict[str, int]:
        """
        Obtiene información sobre el estado del rate limit.
        
        Args:
            identifier: Identificador único (IP, user_id, etc.)
            endpoint: Nombre del endpoint
            limit: Número máximo de solicitudes permitidas
            window: Ventana de tiempo en segundos (default: 60)
        
        Returns:
            Diccionario con remaining_requests y reset_time
        """
        key = RateLimiter._get_key(identifier, endpoint, window)
        current = cache.get(key, 0)
        
        return {
            'limit': limit,
            'used': current,
            'remaining': max(0, limit - current),
            'reset_time': window
        }


class SecurityHeaders:
    """
    Clase para generar headers de seguridad HTTP.
    """
    
    @staticmethod
    def get_headers() -> Dict[str, str]:
        """
        Obtiene diccionario con headers de seguridad recomendados.
        
        Returns:
            Diccionario con headers de seguridad
        """
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https:; "
                "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                "connect-src 'self'; "
                "frame-ancestors 'none'"
            ),
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': (
                'geolocation=(), microphone=(), camera=(), '
                'payment=(), usb=(), magnetometer=(), gyroscope=()'
            )
        }
    
    @staticmethod
    def apply_headers(response) -> None:
        """
        Aplica headers de seguridad a una respuesta HTTP.
        
        Args:
            response: Objeto de respuesta HTTP de Django
        """
        headers = SecurityHeaders.get_headers()
        for key, value in headers.items():
            response[key] = value


def get_client_ip(request) -> str:
    """
    Obtiene la dirección IP del cliente de forma segura.
    Considera proxies y load balancers.
    
    Args:
        request: Objeto de request de Django
    
    Returns:
        Dirección IP del cliente
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    return ip


def get_request_fingerprint(request) -> str:
    """
    Genera un fingerprint único para una request.
    Útil para detectar patrones de ataque.
    
    Args:
        request: Objeto de request de Django
    
    Returns:
        Fingerprint hash
    """
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    session_id = request.COOKIES.get('session_token', 'none')
    
    fingerprint_data = f"{ip}:{user_agent}:{session_id}"
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()
