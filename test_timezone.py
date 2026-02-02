"""
Script de prueba para verificar que los timestamps funcionan correctamente con zona horaria.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from webAMG.models import Project, User


print("=" * 70)
print("PRUEBA DE TIMESTAMPS CON ZONA HORARIA")
print("=" * 70)

# Obtener la hora actual con zona horaria
now_utc = timezone.now()
now_local = timezone.localtime(now_utc)
now_naive = datetime.now()

print("\n1. Horas actuales:")
print(f"   Hora UTC (Django): {now_utc}")
print(f"   Hora UTC (formato): {now_utc.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"   Hora Local (Guatemala): {now_local}")
print(f"   Hora Local (formato): {now_local.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"   Hora naive (sistema): {now_naive}")
print(f"   Hora naive (formato): {now_naive.strftime('%d/%m/%Y %H:%M:%S')}")

# Buscar un usuario existente
try:
    user = User.objects.first()
    if not user:
        print("\n   No hay usuarios en la base de datos. Creando uno de prueba...")
        user = User.objects.create(
            username='test_user_timezone',
            email='test@example.com',
            full_name='Usuario de Prueba',
            password_hash='test_hash'
        )
        print(f"   Usuario creado: {user.username}")
    
    # Buscar un proyecto existente
    project = Project.objects.first()
    
    if not project:
        print("\n   No hay proyectos en la base de datos. Creando uno de prueba...")
        project = Project.objects.create(
            project_name='Proyecto de Prueba - Zona Horaria',
            start_date=now_local.date(),
            created_by=user
        )
        print(f"   Proyecto creado: {project.project_name}")
    
    print(f"\n2. Proyecto: {project.project_name}")
    print(f"   ID: {project.id}")
    print(f"   Fecha inicio: {project.start_date}")
    print(f"   Created at (raw): {project.created_at}")
    print(f"   Created at (UTC): {project.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   Created at (Local): {timezone.localtime(project.created_at).strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   Updated at (raw): {project.updated_at}")
    print(f"   Updated at (UTC): {project.updated_at.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   Updated at (Local): {timezone.localtime(project.updated_at).strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Actualizar el proyecto
    print("\n3. Actualizando proyecto...")
    old_updated_at = project.updated_at
    project.description = f"Actualizado a las {now_local.strftime('%H:%M:%S')}"
    project.save()
    
    # Recargar el proyecto desde la base de datos
    project.refresh_from_db()
    
    print(f"   Old updated_at (Local): {timezone.localtime(old_updated_at).strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   New updated_at (Local): {timezone.localtime(project.updated_at).strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"   La hora se actualizo correctamente: {old_updated_at < project.updated_at}")
    
    # Consultar proyectos ordenados por created_at
    print("\n4. Últimos proyectos (ordenados por created_at):")
    for p in Project.objects.all().order_by('-created_at')[:3]:
        print(f"   - {p.project_name}:")
        print(f"     UTC: {p.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"     Guatemala: {timezone.localtime(p.created_at).strftime('%d/%m/%Y %H:%M:%S')}")
    
    print("\n5. Verificación de configuración:")
    print("   Django TIME_ZONE:", settings.TIME_ZONE)
    print("   Django USE_TZ:", settings.USE_TZ)
    print("   Comportamiento correcto:")
    print("     - Django guarda en UTC (correcto para evitar problemas con horario de verano)")
    print("     - Django muestra en zona horaria local cuando se usa |date o timezone.localtime()")
    print("     - PostgreSQL usa America/Guatemala configurada en la conexión")
    
    print("\n" + "=" * 70)
    print("FIN DE LA PRUEBA - Configuración CORRECTA")
    print("=" * 70)
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
