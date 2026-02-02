"""
Script para verificar las fechas y horas de proyectos y evidencias.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.conf import settings
from datetime import datetime
from webAMG.models import Project, ProjectEvidence

print("=" * 70)
print("VERIFICACIÓN DE FECHAS Y HORAS")
print("=" * 70)

print(f"\nConfiguración de Django:")
print(f"  TIME_ZONE: {settings.TIME_ZONE}")
print(f"  USE_TZ: {settings.USE_TZ}")

now_utc = timezone.now()
now_local = timezone.localtime(now_utc)

print(f"\nHora actual:")
print(f"  UTC: {now_utc.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"  Guatemala: {now_local.strftime('%d/%m/%Y %H:%M:%S')}")

print("\n" + "-" * 70)
print("PROYECTOS")
print("-" * 70)

projects = Project.objects.all().order_by('-updated_at')[:5]

if not projects:
    print("No hay proyectos en la base de datos.")
else:
    for project in projects:
        print(f"\n{project.project_name}:")
        print(f"  ID: {project.id}")
        print(f"  Fecha inicio: {project.start_date}")
        
        created_at_utc = project.created_at
        created_at_local = timezone.localtime(created_at_utc)
        
        updated_at_utc = project.updated_at
        updated_at_local = timezone.localtime(updated_at_utc)
        
        print(f"  Creado (UTC): {created_at_utc.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Creado (GT): {created_at_local.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Actualizado (UTC): {updated_at_utc.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Actualizado (GT): {updated_at_local.strftime('%d/%m/%Y %H:%M:%S')}")
        
        print(f"  Evidencias: {project.evidences.count()}")

print("\n" + "-" * 70)
print("EVIDENCIAS")
print("-" * 70)

evidences = ProjectEvidence.objects.all().order_by('-updated_at')[:5]

if not evidences:
    print("No hay evidencias en la base de datos.")
else:
    for evidence in evidences:
        print(f"\nEvidencia #{evidence.id}:")
        print(f"  Proyecto: {evidence.project.project_name}")
        print(f"  Fecha inicio: {evidence.start_date}")
        print(f"  Fecha fin: {evidence.end_date or 'N/A'}")
        print(f"  Descripción: {evidence.description[:50]}..." if len(evidence.description) > 50 else f"  Descripción: {evidence.description}")
        
        created_at_utc = evidence.created_at
        created_at_local = timezone.localtime(created_at_utc)
        
        updated_at_utc = evidence.updated_at
        updated_at_local = timezone.localtime(updated_at_utc)
        
        print(f"  Creado (UTC): {created_at_utc.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Creado (GT): {created_at_local.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Actualizado (UTC): {updated_at_utc.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Actualizado (GT): {updated_at_local.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"  Fotos: {evidence.photos.count()}")

print("\n" + "=" * 70)
print("FIN DE LA VERIFICACIÓN")
print("=" * 70)

print("\nNOTA:")
print("  - Los timestamps se guardan en UTC (correcto para evitar problemas de horario de verano)")
print("  - Django los convierte automáticamente a Guatemala al mostrarlos en plantillas")
print("  - La diferencia de 6 horas entre UTC y Guatemala es CORRECTA")
print("  - Para ver la hora en Guatemala en Python, usa: timezone.localtime(fecha_utc)")
print("  - En plantillas Django, usa: {{ fecha|date:'d/m/Y H:i' }}")
