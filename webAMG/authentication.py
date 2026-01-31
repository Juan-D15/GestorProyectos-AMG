"""
Backend de autenticación personalizado para el modelo User.
Compatible con el esquema PostgreSQL de BasedeDatos.txt.
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from .models import User


class CustomUserBackend(BaseBackend):
    """
    Backend de autenticación personalizado que usa el modelo User
    con password_hash en lugar del password de Django.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica un usuario usando username y password.
        Verifica el password contra password_hash usando bcrypt.
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            # Buscar usuario por username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Buscar usuario por email como alternativa
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        # Verificar la contraseña
        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        """
        Retorna el usuario con el ID proporcionado.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Verifica si el usuario tiene un permiso específico.
        Los administradores tienen todos los permisos.
        """
        return user_obj.is_admin()

    def has_module_perms(self, user_obj, app_label):
        """
        Verifica si el usuario tiene permisos para un módulo.
        Los administradores tienen acceso a todos los módulos.
        """
        return user_obj.is_admin()
