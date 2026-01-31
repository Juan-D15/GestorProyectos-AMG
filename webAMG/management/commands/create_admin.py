"""
Comando de gestión de Django para crear un usuario administrador por defecto.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un usuario administrador por defecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Nombre de usuario del administrador'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@mayaguatemala.org',
            help='Email del administrador'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='Admin123!',
            help='Contraseña del administrador'
        )
        parser.add_argument(
            '--full-name',
            type=str,
            default='Administrador del Sistema',
            help='Nombre completo del administrador'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        full_name = options['full_name']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe.')
            )
            return

        # Crear usuario administrador
        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            role='administrador',
            is_active=True
        )
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Usuario administrador creado exitosamente:\n'
                f'  Username: {username}\n'
                f'  Email: {email}\n'
                f'  Full Name: {full_name}\n'
                f'  Role: administrador'
            )
        )
