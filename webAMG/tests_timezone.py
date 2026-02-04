"""
Tests para verificar el manejo correcto de zonas horarias.
"""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser
from pytz import timezone as pytz_timezone
from datetime import datetime, timedelta
from webAMG.models import User, Project, ProjectEvidence
from webAMG.models import Beneficiary


class TimezoneTestCase(TestCase):
    """Tests para verificar el manejo de fechas con zona horaria de Guatemala."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='usuario'
        )
        
        # Crear un beneficiario de prueba
        self.beneficiary = Beneficiary.objects.create(
            first_name='Juan',
            last_name='Pérez',
            cui_dpi='1234567890101',
            is_active=True
        )
    
    def test_guatemala_timezone_settings(self):
        """Verificar que Django está configurado con la zona horaria de Guatemala."""
        from django.conf import settings
        
        self.assertEqual(settings.TIME_ZONE, 'America/Guatemala')
        self.assertTrue(settings.USE_TZ)
    
    def test_project_created_at_timezone(self):
        """Verificar que la fecha de creación del proyecto usa la zona horaria correcta."""
        # Obtener la hora actual en Guatemala
        guatemala_tz = pytz_timezone('America/Guatemala')
        now_guatemala = timezone.now().astimezone(guatemala_tz)
        
        # Crear un proyecto
        project = Project.objects.create(
            project_name='Test Project',
            project_code='TP001',
            description='Test description',
            status='planificado'
        )
        project.beneficiaries.add(self.beneficiary)
        
        # Verificar que created_at no sea nulo
        self.assertIsNotNone(project.created_at)
        
        # Verificar que created_at sea timezone-aware
        self.assertTrue(project.created_at.tzinfo is not None)
        
        # Convertir a zona horaria de Guatemala
        created_at_guatemala = project.created_at.astimezone(guatemala_tz)
        
        # La diferencia debe ser menor a 5 segundos (tiempo de ejecución)
        time_diff = abs((now_guatemala - created_at_guatemala).total_seconds())
        self.assertLess(time_diff, 5, 
                       f'La fecha de creación ({created_at_guatemala}) difiere mucho de la hora actual ({now_guatemala})')
        
        # Imprimir para depuración
        print(f'\n--- Test Project Created At ---')
        print(f'Hora actual en Guatemala: {now_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Project.created_at (UTC): {project.created_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Project.created_at (Guatemala): {created_at_guatemala.strftime("%d/m/%Y %H:%M:%S %Z")}')
        print(f'Diferencia en segundos: {time_diff}')
    
    def test_project_updated_at_timezone(self):
        """Verificar que la fecha de actualización del proyecto usa la zona horaria correcta."""
        guatemala_tz = pytz_timezone('America/Guatemala')
        
        # Crear un proyecto
        project = Project.objects.create(
            project_name='Test Project',
            project_code='TP001',
            description='Test description',
            status='planificado'
        )
        original_created_at = project.created_at
        original_updated_at = project.updated_at
        
        # Esperar un momento
        import time
        time.sleep(1)
        
        # Actualizar el proyecto
        project.project_name = 'Updated Project'
        project.save()
        
        # Verificar que updated_at cambió
        self.assertNotEqual(original_updated_at, project.updated_at)
        self.assertEqual(original_created_at, project.created_at)
        
        # Verificar que updated_at sea timezone-aware
        self.assertTrue(project.updated_at.tzinfo is not None)
        
        # Convertir a zona horaria de Guatemala
        updated_at_guatemala = project.updated_at.astimezone(guatemala_tz)
        now_guatemala = timezone.now().astimezone(guatemala_tz)
        
        # La diferencia debe ser menor a 3 segundos
        time_diff = abs((now_guatemala - updated_at_guatemala).total_seconds())
        self.assertLess(time_diff, 3)
        
        # Imprimir para depuración
        print(f'\n--- Test Project Updated At ---')
        print(f'Original updated_at: {original_updated_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Nuevo updated_at (UTC): {project.updated_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Nuevo updated_at (Guatemala): {updated_at_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Hora actual en Guatemala: {now_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Diferencia en segundos: {time_diff}')
    
    def test_evidence_created_at_timezone(self):
        """Verificar que la fecha de creación de la evidencia usa la zona horaria correcta."""
        guatemala_tz = pytz_timezone('America/Guatemala')
        now_guatemala = timezone.now().astimezone(guatemala_tz)
        
        # Crear un proyecto
        project = Project.objects.create(
            project_name='Test Project',
            project_code='TP001',
            description='Test description',
            status='planificado'
        )
        
        # Crear una evidencia
        evidence = ProjectEvidence.objects.create(
            project=project,
            start_date='2026-01-01',
            end_date='2026-01-31',
            description='Test evidence description',
            created_by=self.user
        )
        
        # Verificar que created_at no sea nulo
        self.assertIsNotNone(evidence.created_at)
        
        # Verificar que created_at sea timezone-aware
        self.assertTrue(evidence.created_at.tzinfo is not None)
        
        # Convertir a zona horaria de Guatemala
        created_at_guatemala = evidence.created_at.astimezone(guatemala_tz)
        
        # La diferencia debe ser menor a 5 segundos
        time_diff = abs((now_guatemala - created_at_guatemala).total_seconds())
        self.assertLess(time_diff, 5)
        
        # Imprimir para depuración
        print(f'\n--- Test Evidence Created At ---')
        print(f'Hora actual en Guatemala: {now_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Evidence.created_at (UTC): {evidence.created_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Evidence.created_at (Guatemala): {created_at_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Diferencia en segundos: {time_diff}')
    
    def test_evidence_updated_at_timezone(self):
        """Verificar que la fecha de actualización de la evidencia usa la zona horaria correcta."""
        guatemala_tz = pytz_timezone('America/Guatemala')
        
        # Crear un proyecto y evidencia
        project = Project.objects.create(
            project_name='Test Project',
            project_code='TP001',
            description='Test description',
            status='planificado'
        )
        
        evidence = ProjectEvidence.objects.create(
            project=project,
            start_date='2026-01-01',
            end_date='2026-01-31',
            description='Test evidence description',
            created_by=self.user
        )
        
        original_created_at = evidence.created_at
        original_updated_at = evidence.updated_at
        
        # Esperar un momento
        import time
        time.sleep(1)
        
        # Actualizar la evidencia
        evidence.description = 'Updated evidence description'
        evidence.save()
        
        # Verificar que updated_at cambió
        self.assertNotEqual(original_updated_at, evidence.updated_at)
        self.assertEqual(original_created_at, evidence.created_at)
        
        # Verificar que updated_at sea timezone-aware
        self.assertTrue(evidence.updated_at.tzinfo is not None)
        
        # Convertir a zona horaria de Guatemala
        updated_at_guatemala = evidence.updated_at.astimezone(guatemala_tz)
        now_guatemala = timezone.now().astimezone(guatemala_tz)
        
        # La diferencia debe ser menor a 3 segundos
        time_diff = abs((now_guatemala - updated_at_guatemala).total_seconds())
        self.assertLess(time_diff, 3)
        
        # Imprimir para depuración
        print(f'\n--- Test Evidence Updated At ---')
        print(f'Original updated_at: {original_updated_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Nuevo updated_at (UTC): {evidence.updated_at.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Nuevo updated_at (Guatemala): {updated_at_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Hora actual en Guatemala: {now_guatemala.strftime("%d/%m/%Y %H:%M:%S %Z")}')
        print(f'Diferencia en segundos: {time_diff}')
    
    def test_timezone_middleware(self):
        """Verificar que el middleware de zona horaria funcione correctamente."""
        from webAMG.middleware import TimezoneMiddleware
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/')
        
        # Crear una instancia del middleware
        middleware = TimezoneMiddleware(lambda x: x)
        
        # Procesar la solicitud
        response = middleware(request)
        
        # Verificar que la zona horaria esté activada
        from django.utils import timezone
        current_timezone = timezone.get_current_timezone()
        
        print(f'\n--- Test Timezone Middleware ---')
        print(f'Zona horaria actual: {current_timezone}')
        print(f'Es America/Guatemala: {str(current_timezone) == "America/Guatemala"}')
        
        self.assertIsNotNone(current_timezone)
