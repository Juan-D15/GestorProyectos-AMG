"""
Comando de gestion de Django para verificar la configuracion de zona horaria.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.utils import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Verifica la configuracion de zona horaria de Django y PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('=' * 70)
        self.stdout.write('VERIFICACION DE ZONA HORARIA')
        self.stdout.write('=' * 70)
        
        # Establecer zona horaria en la conexion
        try:
            with connections['default'].cursor() as cursor:
                cursor.execute("SET TIME ZONE 'America/Guatemala'")
        except Exception:
            pass
        
        # Configuracion de Django
        self.stdout.write('\n1. Configuracion de Django:')
        self.stdout.write(f'   TIME_ZONE: {settings.TIME_ZONE}')
        self.stdout.write(f'   USE_TZ: {settings.USE_TZ}')
        self.stdout.write(f'   LANGUAGE_CODE: {settings.LANGUAGE_CODE}')
        
        # Hora actual en Python (sin zona horaria)
        naive_now = datetime.now()
        self.stdout.write(f'\n   Hora Python (naive): {naive_now}')
        
        # Hora actual en Django con zona horaria
        aware_now = timezone.now()
        self.stdout.write(f'   Hora Django (aware): {aware_now}')
        self.stdout.write(f'   Hora Django (timezone info): {aware_now.tzinfo}')
        
        # Formatear hora
        self.stdout.write(f'   Hora formateada (d/m/Y H:i): {aware_now.strftime("%d/%m/%Y %H:%M")}')
        
        # Configuracion de PostgreSQL
        self.stdout.write('\n2. Configuracion de PostgreSQL:')
        try:
            with connections['default'].cursor() as cursor:
                # Verificar zona horaria actual de la conexion
                cursor.execute("SHOW TIME ZONE")
                pg_timezone = cursor.fetchone()[0]
                self.stdout.write(f'   Zona horaria PostgreSQL: {pg_timezone}')
                
                # Verificar hora actual de PostgreSQL
                cursor.execute("SELECT CURRENT_TIMESTAMP, CURRENT_TIMESTAMP AT TIME ZONE 'America/Guatemala'")
                pg_timestamp, pg_guatemala = cursor.fetchone()
                self.stdout.write(f'   Hora PostgreSQL (default): {pg_timestamp}')
                self.stdout.write(f'   Hora PostgreSQL (Guatemala): {pg_guatemala}')
                
                # Verificar si las horas coinciden
                # Django usa UTC internamente (correcto), pero debe ser convertido a Guatemala para mostrar
                # Convertir Django UTC a Guatemala para comparación
                django_guatemala = timezone.localtime(aware_now)
                django_guatemala_str = django_guatemala.strftime("%Y-%m-%d %H:%M:%S")
                pg_guatemala_str = pg_guatemala.strftime("%Y-%m-%d %H:%M:%S")
                
                # Verificar la diferencia (debe ser muy pequeña, menos de 1 segundo)
                time_diff = abs((django_guatemala - pg_guatemala.replace(tzinfo=django_guatemala.tzinfo)).total_seconds())
                
                if time_diff < 2:
                    self.stdout.write(self.style.SUCCESS('\n   Las horas de PostgreSQL y Django coinciden correctamente!'))
                    self.stdout.write(f'   - Django UTC: {aware_now.strftime("%Y-%m-%d %H:%M:%S")}')
                    self.stdout.write(f'   - Django Guatemala: {django_guatemala_str}')
                    self.stdout.write(f'   - PostgreSQL Guatemala: {pg_guatemala_str}')
                    self.stdout.write(f'   - Diferencia: {time_diff:.3f} segundos')
                else:
                    self.stdout.write(self.style.ERROR(f'\n   Las horas NO coinciden:'))
                    self.stdout.write(f'      Django (UTC): {aware_now.strftime("%Y-%m-%d %H:%M:%S")}')
                    self.stdout.write(f'      Django (Guatemala): {django_guatemala_str}')
                    self.stdout.write(f'      PostgreSQL (Guatemala): {pg_guatemala_str}')
                    self.stdout.write(f'      Diferencia: {time_diff:.3f} segundos')
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   Error al conectar a PostgreSQL: {e}'))
        
        # Informacion del sistema
        import time
        import os
        
        self.stdout.write('\n3. Informacion del sistema:')
        self.stdout.write(f'   Zona horaria del sistema (TZ): {os.environ.get("TZ", "No configurada")}')
        self.stdout.write(f'   Hora del sistema: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write('FIN DE LA VERIFICACION')
        self.stdout.write('=' * 70)
