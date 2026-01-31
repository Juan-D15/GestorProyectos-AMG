"""
Servicios de autenticación para el sistema.
"""
import secrets
import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from webAMG.models import User, LoginLog, UserSession


class AuthService:
    """Servicio para gestionar la autenticación de usuarios."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro de la contraseña usando SHA-256.
        Nota: En producción, usar bcrypt o Argon2.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verifica si la contraseña coincide con el hash.
        """
        return AuthService.hash_password(password) == password_hash

    @staticmethod
    def login(username: str, password: str, ip_address: str = None, user_agent: str = None):
        """
        Intenta iniciar sesión de un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            ip_address: Dirección IP del cliente
            user_agent: User agent del cliente
            
        Returns:
            dict con éxito/error y datos del usuario si es exitoso
        """
        try:
            # Buscar usuario por username
            user = User.objects.get(username=username, is_active=True)
            
            # Verificar contraseña
            # Nota: Django usa check_password para contraseñas hasheadas
            if user.check_password(password):
                # Registrar login exitoso
                LoginLog.objects.create(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=True
                )
                
                # Actualizar último login
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                # Crear sesión
                session_token = AuthService._generate_session_token()
                expires_at = timezone.now() + timedelta(hours=8)  # 8 horas de sesión
                
                session = UserSession.objects.create(
                    user=user,
                    session_token=session_token,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    expires_at=expires_at
                )
                
                return {
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'full_name': user.full_name,
                        'role': user.role,
                        'profile_image_url': user.profile_image_url,
                    },
                    'session_token': session_token,
                    'expires_at': expires_at.isoformat()
                }
            else:
                # Contraseña incorrecta
                LoginLog.objects.create(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=False,
                    failure_reason='Contraseña incorrecta'
                )
                
                return {
                    'success': False,
                    'error': 'Credenciales inválidas'
                }
                
        except User.DoesNotExist:
            # Usuario no encontrado
            LoginLog.objects.create(
                user=None,
                ip_address=ip_address,
                user_agent=user_agent,
                success=False,
                failure_reason='Usuario no encontrado'
            )
            
            return {
                'success': False,
                'error': 'Credenciales inválidas'
            }

    @staticmethod
    def logout(session_token: str) -> dict:
        """
        Cierra la sesión del usuario.
        
        Args:
            session_token: Token de sesión
            
        Returns:
            dict con resultado de la operación
        """
        try:
            session = UserSession.objects.get(session_token=session_token, is_active=True)
            session.is_active = False
            session.save(update_fields=['is_active'])
            
            return {
                'success': True,
                'message': 'Sesión cerrada exitosamente'
            }
        except UserSession.DoesNotExist:
            return {
                'success': False,
                'error': 'Sesión no encontrada'
            }

    @staticmethod
    def verify_session(session_token: str) -> dict:
        """
        Verifica si una sesión es válida y no ha expirado.
        
        Args:
            session_token: Token de sesión
            
        Returns:
            dict con información del usuario si la sesión es válida
        """
        try:
            session = UserSession.objects.get(
                session_token=session_token,
                is_active=True
            )
            
            # Verificar si expiró
            if session.is_expired():
                session.is_active = False
                session.save(update_fields=['is_active'])
                
                return {
                    'valid': False,
                    'error': 'Sesión expirada'
                }
            
            # Actualizar última actividad
            session.last_activity = timezone.now()
            session.save(update_fields=['last_activity'])
            
            return {
                'valid': True,
                'user': {
                    'id': session.user.id,
                    'username': session.user.username,
                    'email': session.user.email,
                    'full_name': session.user.full_name,
                    'role': session.user.role,
                    'profile_image_url': session.user.profile_image_url,
                }
            }
            
        except UserSession.DoesNotExist:
            return {
                'valid': False,
                'error': 'Sesión no válida'
            }

    @staticmethod
    def _generate_session_token() -> str:
        """
        Genera un token de sesión seguro y único.
        """
        return secrets.token_urlsafe(64)

    @staticmethod
    def get_user_from_session(session_token: str):
        """
        Obtiene el usuario a partir de un token de sesión.
        
        Args:
            session_token: Token de sesión
            
        Returns:
            User object o None si no es válido
        """
        result = AuthService.verify_session(session_token)
        if result['valid']:
            try:
                return User.objects.get(id=result['user']['id'])
            except User.DoesNotExist:
                return None
        return None

    @staticmethod
    def clean_expired_sessions() -> int:
        """
        Limpia las sesiones expiradas de la base de datos.
        
        Returns:
            Número de sesiones eliminadas
        """
        count, _ = UserSession.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True
        ).update(is_active=False)
        
        return count
