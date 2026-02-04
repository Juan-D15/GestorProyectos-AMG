"""
Vistas para renderizar páginas HTML de la aplicación.
Este módulo contiene todas las vistas que renderizan plantillas HTML.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.db import models
from django.utils import timezone
from datetime import datetime
import re
from .forms import LoginForm


def validate_location_name(text):
    """
    Valida que un nombre de ubicación (municipio/departamento) solo contenga
    letras, espacios, tildes y ñ.
    """
    if not text:
        return False
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$'
    return bool(re.match(pattern, text))



@method_decorator(ensure_csrf_cookie, name='dispatch')
class IndexView(TemplateView):
    """Vista de la página principal."""
    template_name = "index.html"


def index(request):
    """
    Vista de la página principal (versión funcional).
    Renderiza la plantilla index.html con los componentes de ReactPy.
    """
    return render(request, "index.html")


# =====================================================
# VISTAS DE AUTENTICACIÓN (PÁGINAS HTML)
# =====================================================

@ensure_csrf_cookie
def login_page(request):
    """
    Vista de la página de login.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Bienvenido, {user.full_name}!')
                    next_url = request.GET.get('next', '/dashboard/')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Su cuenta está inactiva. Contacte al administrador.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, "auth/login.html", {'form': form})


@login_required
def logout_page(request):
    """
    Vista para cerrar sesión y redirigir al login.
    """
    logout(request)
    return render(request, "auth/login.html", {'form': LoginForm(), 'logout_message': True})


# =====================================================
# VISTA DEL DASHBOARD
# =====================================================

@login_required
def dashboard(request):
    """
    Vista del panel principal (dashboard).
    """
    user = request.user
    
    return render(request, "dashboard/index.html", {
        'user': user,
    })


# =====================================================
# VISTAS DE SECCIONES DEL DASHBOARD
# =====================================================

@login_required
def projects_page(request):
    """Vista de la sección Proyectos."""
    return render(request, "dashboard/projects.html", {'user': request.user})




@login_required
def beneficiaries_page(request):
    """Vista de la sección Beneficiarios."""
    from .models import Beneficiary
    
    beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('-created_at')
    
    return render(request, "dashboard/beneficiaries.html", {
        'user': request.user,
        'beneficiaries': beneficiaries
    })


@login_required
def budget_page(request):
    """Vista de la sección Ejecución Presupuestaria."""
    return render(request, "dashboard/budget.html", {'user': request.user})


@login_required
def reports_page(request):
    """Vista de la sección Reportes."""
    return render(request, "dashboard/reports.html", {'user': request.user})


@login_required
def statistics_page(request):
    """Vista de la sección Estadísticas."""
    return render(request, "dashboard/statistics.html", {'user': request.user})


@login_required
def profile_page(request):
    """Vista del perfil de usuario."""
    return render(request, "dashboard/profile.html", {'user': request.user})


# =====================================================
# VISTAS DE GESTIÓN DE USUARIOS (Solo administradores)
# =====================================================

@login_required
def dashboard_users(request):
    """
    Vista de la sección de gestión de usuarios.
    Solo accesible para usuarios con rol 'administrador'.
    """
    if request.user.role != 'administrador':
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('dashboard')
    
    users = request.user.__class__.objects.all()
    return render(request, "dashboard/users.html", {'user': request.user, 'users': users})


@login_required
def user_create(request):
    """
    Vista para crear un nuevo usuario.
    Solo accesible para usuarios con rol 'administrador'.
    """
    if request.user.role != 'administrador':
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')
        role = request.POST.get('role')
        # Los nuevos usuarios se crean activos por defecto
        is_active = True
        
        # Validaciones
        if not all([username, email, full_name, password, role]):
            messages.error(request, 'Todos los campos marcados con * son obligatorios.')
            return redirect('dashboard_users')
        
        if len(password) < 6:
            messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
            return redirect('dashboard_users')
        
        if role not in ['usuario', 'administrador']:
            messages.error(request, 'Rol inválido.')
            return redirect('dashboard_users')
        
        # Verificar si el usuario ya existe
        User = request.user.__class__
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return redirect('dashboard_users')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('dashboard_users')
        
        # Crear el usuario
        try:
            user = User.objects.create(
                username=username,
                email=email,
                full_name=full_name,
                password_hash='',  # Se establecerá después
                phone=phone,
                role=role,
                is_active=True,  # Siempre activo por defecto
            )
            user.set_password(password)
            user.save()
            messages.success(request, f'Usuario {username} creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
        
        return redirect('dashboard_users')
    
    return redirect('dashboard_users')


@login_required
def user_edit(request):
    """
    Vista para editar un usuario existente.
    Solo accesible para usuarios con rol 'administrador'.
    """
    if request.user.role != 'administrador':
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '')
        role = request.POST.get('role')
        is_active = request.POST.get('is_active') == 'on'
        
        # Validaciones
        if not all([user_id, username, email, full_name, role]):
            messages.error(request, 'Todos los campos marcados con * son obligatorios.')
            return redirect('dashboard_users')
        
        if role not in ['usuario', 'administrador']:
            messages.error(request, 'Rol inválido.')
            return redirect('dashboard_users')
        
        User = request.user.__class__
        try:
            user = User.objects.get(id=user_id)
            
            # Verificar si el username ya existe para otro usuario
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('dashboard_users')
            
            # Verificar si el email ya existe para otro usuario
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                messages.error(request, 'El email ya está registrado.')
                return redirect('dashboard_users')
            
            # Actualizar el usuario
            user.username = username
            user.email = email
            user.full_name = full_name
            user.phone = phone
            user.role = role
            user.is_active = is_active
            
            # Actualizar contraseña si se proporcionó
            if password and len(password) >= 6:
                user.set_password(password)
            elif password and len(password) < 6:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
                return redirect('dashboard_users')
            
            user.save()
            messages.success(request, f'Usuario {username} actualizado exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al actualizar usuario: {str(e)}')
        
        return redirect('dashboard_users')
    
    return redirect('dashboard_users')


@login_required
def user_delete(request):
    """
    Vista para eliminar un usuario.
    Solo accesible para usuarios con rol 'administrador'.
    Revalida la contraseña del administrador antes de eliminar.
    """
    if request.user.role != 'administrador':
        messages.error(request, 'No tienes permisos para eliminar usuarios.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        admin_password = request.POST.get('admin_password')
        
        # Depuración
        print(f"DEBUG: user_id={user_id}, admin_password={admin_password}")
        
        if not user_id:
            messages.error(request, 'ID de usuario no proporcionado.')
            return redirect('dashboard_users')
        
        if not admin_password:
            messages.error(request, 'Debes ingresar tu contraseña de administrador para eliminar un usuario.')
            return redirect('dashboard_users')
        
        User = request.user.__class__
        try:
            user = User.objects.get(id=user_id)
            
            # Prevenir autoeliminación
            if user.id == request.user.id:
                messages.error(request, 'No puedes eliminar tu propio usuario.')
                return redirect('dashboard_users')
            
            # Validar contraseña del administrador
            if not request.user.check_password(admin_password):
                messages.error(request, 'La contraseña del administrador es incorrecta. Por seguridad, intenta de nuevo en 3 segundos.')
                return redirect('dashboard_users')
            
            username = user.username
            user.delete()
            messages.success(request, f'Usuario {username} eliminado exitosamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al eliminar usuario: {str(e)}')
            print(f"DEBUG: Exception: {e}")
        
        return redirect('dashboard_users')
    
    return redirect('dashboard_users')


# =====================================================
# VISTAS DE GESTIÓN DE PROYECTOS
# =====================================================

@login_required
def project_create_page(request):
    """
    Vista para crear un nuevo proyecto.
    """
    import time
    import os
    from django.conf import settings
    from webAMG.models import Project, ProjectStatus, Beneficiary
    
    # Consultar beneficiarios activos para mostrar en el modal
    beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    # Debug: Verificar beneficiarios
    print(f'Beneficiarios encontrados: {beneficiaries.count()}')
    for b in beneficiaries:
        print(f'  - ID: {b.id}, Nombre: {b.first_name} {b.last_name}, DPI: {b.cui_dpi}, Activo: {b.is_active}')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            project_name = request.POST.get('project_name')
            project_code = request.POST.get('project_code')
            description = request.POST.get('description')
            objectives = request.POST.get('objectives')
            what_is_done = request.POST.get('what_is_done')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            estimated_budget = request.POST.get('estimated_budget')
            actual_budget = request.POST.get('actual_budget')
            location = request.POST.get('location')
            municipality = request.POST.get('municipality')
            department = request.POST.get('department')
            status = request.POST.get('status', ProjectStatus.PLANIFICADO)
            has_phases = request.POST.get('has_phases') == 'on'
            progress_percentage = request.POST.get('progress_percentage', 0)
            
            # Validar código de proyecto si se proporciona
            if project_code:
                existing_project = Project.objects.filter(project_code=project_code).first()
                if existing_project:
                    messages.error(request, f'El código de proyecto "{project_code}" ya está en uso. Por favor, use otro código.')
                    return render(request, "dashboard/project_create.html", {
                        'user': request.user,
                        'beneficiaries': beneficiaries,
                        'error_project_code': project_code,
                        'error_municipality': municipality,
                        'error_department': department,
                    })
             
            # Validar municipio (solo letras, espacios, tildes y ñ)
            if municipality and not validate_location_name(municipality):
                messages.error(request, 'El municipio solo puede contener letras y espacios. No se permiten números ni caracteres especiales.')
                return render(request, "dashboard/project_create.html", {
                    'user': request.user,
                    'beneficiaries': beneficiaries,
                    'error_project_code': project_code,
                    'error_municipality': municipality,
                    'error_department': department,
                })
             
            # Validar departamento (solo letras, espacios, tildes y ñ)
            if department and not validate_location_name(department):
                messages.error(request, 'El departamento solo puede contener letras y espacios. No se permiten números ni caracteres especiales.')
                return render(request, "dashboard/project_create.html", {
                    'user': request.user,
                    'beneficiaries': beneficiaries,
                    'error_project_code': project_code,
                    'error_municipality': municipality,
                    'error_department': department,
                })
            
            # Manejar imagen de portada
            cover_image_url = None
            if 'cover_image' in request.FILES:
                uploaded_file = request.FILES['cover_image']
                # Crear directorio si no existe
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'FotosPortada')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generar nombre único para el archivo
                file_extension = os.path.splitext(uploaded_file.name)[1]
                unique_filename = f"project_{project_name.replace(' ', '_')}_{int(time.time())}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                # Guardar el archivo
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Guardar la ruta relativa para la base de datos
                cover_image_url = os.path.join('Proyectos', 'FotosPortada', unique_filename).replace('\\', '/')
            
            # Crear el proyecto
            project = Project.objects.create(
                project_name=project_name,
                project_code=project_code if project_code else None,
                description=description,
                objectives=objectives,
                what_is_done=what_is_done,
                start_date=start_date,
                end_date=end_date if end_date else None,
                estimated_budget=estimated_budget if estimated_budget else None,
                actual_budget=actual_budget if actual_budget else None,
                cover_image_url=cover_image_url,
                location=location,
                municipality=municipality,
                department=department,
                status=status,
                has_phases=has_phases,
                progress_percentage=progress_percentage,
                created_by=request.user,
                responsible_user=request.user
            )
            
            # Guardar los beneficiarios seleccionados
            beneficiaries_ids = request.POST.get('beneficiaries', '')
            if beneficiaries_ids:
                # Convertir la cadena de IDs separados por comas en una lista
                beneficiaries_list = [int(id.strip()) for id in beneficiaries_ids.split(',') if id.strip()]
                if beneficiaries_list:
                    project.beneficiaries.set(beneficiaries_list)
                    print(f'Beneficiarios asignados al proyecto: {len(beneficiaries_list)}')
                    print(f'IDs de beneficiarios: {beneficiaries_list}')
            
            messages.success(request, f'Proyecto "{project_name}" creado exitosamente.')
            return redirect('dashboard_projects')
            
        except Exception as e:
            messages.error(request, f'Error al crear el proyecto: {str(e)}')
            print(f"DEBUG: Exception: {e}")
    
    return render(request, "dashboard/project_create.html", {
        'user': request.user,
        'beneficiaries': beneficiaries
    })


@login_required
def project_list_page(request):
    """
    Vista para listar todos los proyectos con filtros.
    """
    from webAMG.models import Project
    
    projects = Project.objects.all().order_by('-created_at')
    
    # Filtros
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        projects = projects.filter(
            models.Q(project_name__icontains=search_query) |
            models.Q(project_code__icontains=search_query) |
            models.Q(location__icontains=search_query)
        )
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    context = {
        'user': request.user,
        'projects': projects,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, "dashboard/project_list.html", context)


@login_required
def project_detail_page(request, project_id):
    """
    Vista para ver detalles de un proyecto específico.
    """
    from webAMG.models import Project, ProjectBeneficiary, Beneficiary, ProjectEvidence, ProjectPhase, PhaseBeneficiary

    project = get_object_or_404(Project, id=project_id)

    print(f'=== DEBUG: Detalles del proyecto {project_id} ===')
    print(f'Nombre del proyecto: {project.project_name}')

    # Obtener los beneficiarios del proyecto usando el modelo intermedio
    beneficiary_assignments = ProjectBeneficiary.objects.filter(project=project)
    print(f'Asignaciones de beneficiarios encontradas: {beneficiary_assignments.count()}')

    beneficiary_ids = beneficiary_assignments.values_list('beneficiary_id', flat=True)
    print(f'IDs de beneficiarios: {beneficiary_ids}')

    beneficiaries = Beneficiary.objects.filter(
        id__in=beneficiary_ids,
        is_active=True
    ).order_by('first_name', 'last_name')

    print(f'Beneficiarios encontrados: {beneficiaries.count()}')
    for b in beneficiaries:
        print(f'  - {b.id}: {b.first_name} {b.last_name}')

    # Obtener las evidencias del proyecto (solo si no tiene fases)
    evidences = ProjectEvidence.objects.filter(project=project).order_by('-start_date', '-created_at')
    print(f'Evidencias encontradas: {evidences.count()}')

    # Obtener las fases del proyecto
    phases = ProjectPhase.objects.filter(project=project).order_by('phase_number')
    print(f'Fases encontradas: {phases.count()}')

    # Obtener los IDs de beneficiarios de cada fase
    phases_beneficiaries = {}
    for phase in phases:
        phase_beneficiaries_assignments = PhaseBeneficiary.objects.filter(phase=phase)
        phases_beneficiaries[phase.id] = list(phase_beneficiaries_assignments.values_list('beneficiary_id', flat=True))

    # Obtener todos los beneficiarios para el modal
    all_beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('first_name', 'last_name')

    context = {
        'user': request.user,
        'project': project,
        'project_beneficiaries': beneficiaries,
        'evidences': evidences,
        'phases': phases,
        'phases_beneficiaries': phases_beneficiaries,
        'all_beneficiaries': all_beneficiaries,
    }

    return render(request, "dashboard/project_detail.html", context)


@login_required
def project_edit_page(request, project_id):
    """
    Vista para editar un proyecto existente.
    Solo permite editar ciertos campos del formulario de creación.
    """
    import time
    import os
    from django.conf import settings
    from webAMG.models import Project, ProjectStatus, Beneficiary, ProjectBeneficiary
    
    project = get_object_or_404(Project, id=project_id)
    
    # Consultar beneficiarios activos para mostrar en el modal
    beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    # Obtener los beneficiarios ya asignados al proyecto
    project_beneficiaries_assignments = ProjectBeneficiary.objects.filter(project=project)
    selected_beneficiary_ids = list(project_beneficiaries_assignments.values_list('beneficiary_id', flat=True))
    
    # Obtener los objetos completos de beneficiarios asignados al proyecto
    project_bbeneficiaries = Beneficiary.objects.filter(
        id__in=selected_beneficiary_ids,
        is_active=True
    ).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        try:
            # Campos editables del formulario de creación
            project.project_name = request.POST.get('project_name', project.project_name)
            project.project_code = request.POST.get('project_code') or project.project_code
            project.description = request.POST.get('description') or project.description
            project.objectives = request.POST.get('objectives') or project.objectives
            project.what_is_done = request.POST.get('what_is_done') or project.what_is_done
            
            # Mantener fechas existentes si no se envían nuevos valores
            start_date = request.POST.get('start_date')
            if start_date:
                project.start_date = start_date
            
            end_date = request.POST.get('end_date')
            if end_date:
                project.end_date = end_date
            
            project.estimated_budget = request.POST.get('estimated_budget') or project.estimated_budget
            project.actual_budget = request.POST.get('actual_budget') or project.actual_budget
            project.location = request.POST.get('location') or project.location
             
            # Validar municipio y departamento (solo letras, espacios, tildes y ñ)
            municipality = request.POST.get('municipality')
            department = request.POST.get('department')
             
            if municipality and not validate_location_name(municipality):
                messages.error(request, 'El municipio solo puede contener letras y espacios. No se permiten números ni caracteres especiales.')
                return render(request, "dashboard/project_edit.html", {
                    'user': request.user,
                    'project': project,
                    'beneficiaries': beneficiaries,
                    'selected_beneficiary_ids': selected_beneficiary_ids,
                    'project_bbeneficiaries': project_bbeneficiaries,
                    'error_municipality': municipality,
                    'error_department': department,
                 })
            
            if department and not validate_location_name(department):
                messages.error(request, 'El departamento solo puede contener letras y espacios. No se permiten números ni caracteres especiales.')
                return render(request, "dashboard/project_edit.html", {
                    'user': request.user,
                    'project': project,
                    'beneficiaries': beneficiaries,
                    'selected_beneficiary_ids': selected_beneficiary_ids,
                    'project_bbeneficiaries': project_bbeneficiaries,
                    'error_municipality': municipality,
                    'error_department': department,
                })
            
            project.municipality = municipality or project.municipality
            project.department = department or project.department
            project.status = request.POST.get('status', project.status)
            project.has_phases = request.POST.get('has_phases') == 'on'
            project.progress_percentage = request.POST.get('progress_percentage', 0) or project.progress_percentage
            
            # Eliminar imagen de portada si se marca el checkbox
            if request.POST.get('remove_cover_image'):
                if project.cover_image_url:
                    # Eliminar el archivo del sistema de archivos
                    image_path = os.path.join(settings.MEDIA_ROOT, project.cover_image_url)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f'Imagen eliminada: {image_path}')
                    # Eliminar la referencia en la base de datos
                    project.cover_image_url = None
            
            # Manejar imagen de portada si se sube una nueva
            if 'cover_image' in request.FILES:
                uploaded_file = request.FILES['cover_image']
                # Crear directorio si no existe
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'FotosPortada')
                os.makedirs(upload_dir, exist_ok=True)
                 
                # Generar nombre único para el archivo
                file_extension = os.path.splitext(uploaded_file.name)[1]
                unique_filename = f"project_{project.project_name.replace(' ', '_')}_{int(time.time())}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)
                 
                # Guardar el archivo
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                 
                # Guardar la ruta relativa para la base de datos
                project.cover_image_url = os.path.join('Proyectos', 'FotosPortada', unique_filename).replace('\\', '/')
            
            # Guardar el proyecto
            project.save()


            
            # Actualizar los beneficiarios seleccionados
            beneficiaries_ids = request.POST.get('beneficiaries', '')
            if beneficiaries_ids:
                # Convertir la cadena de IDs separados por comas en una lista
                beneficiaries_list = [int(id.strip()) for id in beneficiaries_ids.split(',') if id.strip()]
                if beneficiaries_list:
                    project.beneficiaries.set(beneficiaries_list)
                    print(f'Beneficiarios actualizados en el proyecto: {len(beneficiaries_list)}')
                    print(f'IDs de beneficiarios: {beneficiaries_list}')
            else:
                project.beneficiaries.clear()
                print('Beneficiarios eliminados del proyecto')
            
            messages.success(request, f'Proyecto "{project.project_name}" actualizado exitosamente.')
            return redirect('project_list')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el proyecto: {str(e)}')
            print(f"DEBUG: Exception: {e}")
    
    return render(request, "dashboard/project_edit.html", {
        'user': request.user,
        'project': project,
        'beneficiaries': beneficiaries,
        'selected_beneficiary_ids': selected_beneficiary_ids,
        'project_bbeneficiaries': project_bbeneficiaries
    })


@login_required
def project_delete_page(request, project_id):
    """
    Vista para eliminar un proyecto.
    Requiere validación de contraseña.
    """
    import os
    from django.conf import settings
    from webAMG.models import Project
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Validar que se haya ingresado la contraseña
        if not password:
            messages.error(request, 'Debe ingresar su contraseña para eliminar el proyecto.')
            return render(request, "dashboard/project_delete.html", {
                 'user': request.user,
                 'project': project
              })
        
        # Validar la contraseña del usuario
        if not request.user.check_password(password):
            messages.error(request, 'Contraseña incorrecta. No se puede eliminar el proyecto.')
            return render(request, "dashboard/project_delete.html", {
                'user': request.user,
                'project': project
            })
        
        try:
            project_name = project.project_name
            
            # Eliminar la imagen de portada si existe
            if project.cover_image_url:
                image_path = os.path.join(settings.MEDIA_ROOT, project.cover_image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f'Imagen eliminada: {image_path}')
            
            # Eliminar el proyecto
            project.delete()
            messages.success(request, f'Proyecto "{project_name}" eliminado exitosamente.')
            return redirect('project_list')
        except Exception as e:
            messages.error(request, f'Error al eliminar el proyecto: {str(e)}')
            return redirect('project_detail', project_id=project.id)
    
    return render(request, "dashboard/project_delete.html", {
        'user': request.user,
        'project': project
    })





# =====================================================
# VISTAS DE EVIDENCIAS
# =====================================================

@login_required
def project_evidence_add(request, project_id):
    """
    Vista para agregar una evidencia a un proyecto.
    """
    import time
    import os
    from django.conf import settings
    from webAMG.models import Project, ProjectEvidence, EvidencePhoto, EvidenceBeneficiary, Beneficiary
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        try:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')
            
            # Validar fechas
            if not start_date:
                messages.error(request, 'Debe especificar la fecha de inicio.')
                return redirect('project_detail', project_id=project_id)
            
            # Si no se especifica fecha de fin, usar la fecha de inicio
            if not end_date:
                end_date = start_date
            
            if end_date < start_date:
                messages.error(request, 'La fecha de fin debe ser posterior o igual a la fecha de inicio.')
                return redirect('project_detail', project_id=project_id)
            
            if not description:
                messages.error(request, 'Debe proporcionar una descripción de la evidencia.')
                return redirect('project_detail', project_id=project_id)
             
            # Crear la evidencia
            evidence = ProjectEvidence.objects.create(
                project=project,
                start_date=start_date,
                end_date=end_date,
                description=description,
                created_by=request.user
            )
            
            # Actualizar SOLO el updated_at del proyecto SIN afectar created_at
            project.updated_at = timezone.now()
            project.save(update_fields=['updated_at'])
            
            # Procesar beneficiarios
            beneficiaries_ids = request.POST.get('beneficiaries', '').split(',')
            beneficiaries_ids = [int(b_id.strip()) for b_id in beneficiaries_ids if b_id.strip().isdigit()]
            
            print(f'Beneficiarios a asignar: {beneficiaries_ids}')
            
            for beneficiary_id in beneficiaries_ids:
                try:
                    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                    EvidenceBeneficiary.objects.create(
                        evidence=evidence,
                        beneficiary=beneficiary
                    )
                    print(f'Beneficiario {beneficiary_id} asignado a la evidencia')
                except Beneficiary.DoesNotExist:
                    print(f'Beneficiario {beneficiary_id} no encontrado, omitiendo')
            
            # Procesar fotos
            photos = request.FILES.getlist('photos')
            print(f'=== DEBUG: Creando nueva evidencia ===')
            print(f'Evidencia ID: {evidence.id}')
            print(f'Fotos recibidas: {len(photos)}')
            
            if photos:
                # Crear directorio si no existe
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'Evidencias')
                os.makedirs(upload_dir, exist_ok=True)
                
                for i, photo in enumerate(photos, start=1):
                    # Generar nombre único para el archivo
                    file_extension = os.path.splitext(photo.name)[1]
                    unique_filename = f"evidence_{project.id}_{evidence.id}_{int(time.time())}_{i}{file_extension}"
                    file_path = os.path.join(upload_dir, unique_filename)
                    
                    # Guardar el archivo
                    with open(file_path, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                    
                    # Guardar la foto en la base de datos
                    new_photo = EvidencePhoto.objects.create(
                        evidence=evidence,
                        photo_url=os.path.join('Proyectos', 'Evidencias', unique_filename).replace('\\', '/'),
                        photo_order=i,
                        uploaded_by=request.user
                    )
                    print(f'  Foto {i}: {photo.name} -> ID={new_photo.id}, archivo={unique_filename}')
                
                print(f'Total de fotos guardadas: {len(photos)}')
            else:
                print('No se recibieron fotos')
            
            print(f'=== FIN DEBUG: Creando evidencia ===')
            
            messages.success(request, f'Evidencia agregada exitosamente al proyecto "{project.project_name}".')
            return redirect('project_detail', project_id=project_id)
            
        except Exception as e:
            messages.error(request, f'Error al agregar la evidencia: {str(e)}')
            print(f"DEBUG: Exception: {e}")
    
    return redirect('project_detail', project_id=project_id)


@login_required
def phase_create(request, project_id):
    """
    Vista para crear una nueva fase en un proyecto.
    """
    from webAMG.models import Project, ProjectPhase, PhaseBeneficiary, Beneficiary

    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        try:
            phase_name = request.POST.get('phase_name')
            description = request.POST.get('description')
            status = request.POST.get('status', 'pendiente')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            beneficiaries_input = request.POST.get('beneficiaries')

            if not phase_name:
                messages.error(request, 'Debe especificar el nombre de la fase.')
                return redirect('project_detail', project_id=project_id)

            if not start_date:
                messages.error(request, 'Debe especificar la fecha de inicio.')
                return redirect('project_detail', project_id=project_id)

            if not end_date:
                end_date = start_date

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if end_date < start_date:
                messages.error(request, 'La fecha de fin debe ser posterior o igual a la fecha de inicio.')
                return redirect('project_detail', project_id=project_id)

            # Calcular el siguiente número de fase
            last_phase = ProjectPhase.objects.filter(project=project).order_by('-phase_number').first()
            phase_number = (last_phase.phase_number + 1) if last_phase else 1

            phase = ProjectPhase.objects.create(
                project=project,
                phase_name=phase_name,
                phase_number=phase_number,
                description=description,
                status=status,
                start_date=start_date,
                end_date=end_date,
                created_by=request.user
            )

            if beneficiaries_input:
                beneficiary_ids = [int(bid.strip()) for bid in beneficiaries_input.split(',') if bid.strip().isdigit()]
                for beneficiary_id in beneficiary_ids:
                    try:
                        beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                        PhaseBeneficiary.objects.get_or_create(
                            phase=phase,
                            beneficiary=beneficiary
                        )
                    except Beneficiary.DoesNotExist:
                        continue

            messages.success(request, f'Fase "{phase_name}" creada exitosamente.')
            return redirect('project_detail', project_id=project_id)

        except Exception as e:
            messages.error(request, f'Error al crear la fase: {str(e)}')
            print(f"ERROR: Exception in phase_create: {e}")
            return redirect('project_detail', project_id=project_id)

    return redirect('project_detail', project_id=project_id)


@login_required
def phase_edit(request, project_id, phase_id):
    """
    Vista para editar una fase existente.
    Solo permite editar ciertos campos del formulario de creación.
    """
    from webAMG.models import Project, ProjectPhase, PhaseBeneficiary, Beneficiary

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)

    if request.method == 'POST':
        try:
            phase_name = request.POST.get('phase_name')
            description = request.POST.get('description')
            status = request.POST.get('status')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Validar campos requeridos
            if not phase_name:
                messages.error(request, 'Debe especificar el nombre de la fase.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            if not start_date:
                messages.error(request, 'Debe especificar la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            # Si no se especifica fecha de fin, usar la fecha de inicio
            if not end_date:
                end_date = start_date

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if end_date < start_date:
                messages.error(request, 'La fecha de fin debe ser posterior o igual a la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            # Actualizar la fase
            phase.phase_name = phase_name
            phase.description = description
            phase.status = status
            phase.start_date = start_date
            phase.end_date = end_date
            phase.save()

            # Actualizar el updated_at del proyecto
            project.updated_at = timezone.now()
            project.save(update_fields=['updated_at'])

            # Eliminar beneficiarios existentes y volver a agregarlos
            PhaseBeneficiary.objects.filter(phase=phase).delete()
            beneficiaries_ids = request.POST.get('beneficiaries', '').split(',')
            beneficiaries_ids = [int(b_id.strip()) for b_id in beneficiaries_ids if b_id.strip().isdigit()]

            for beneficiary_id in beneficiaries_ids:
                try:
                    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                    PhaseBeneficiary.objects.create(
                        phase=phase,
                        beneficiary=beneficiary,
                        created_by=request.user
                    )
                except Beneficiary.DoesNotExist:
                    pass

            messages.success(request, f'Fase "{phase_name}" actualizada exitosamente.')
            return redirect('project_detail', project_id=project_id)

        except Exception as e:
            messages.error(request, f'Error al actualizar la fase: {str(e)}')
            return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

    # Obtener todos los beneficiarios disponibles
    all_beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('first_name', 'last_name')

    # Obtener los IDs de beneficiarios de esta fase
    phase_beneficiaries_assignments = PhaseBeneficiary.objects.filter(phase=phase)
    selected_beneficiary_ids = list(phase_beneficiaries_assignments.values_list('beneficiary_id', flat=True))

    # Obtener los objetos completos de beneficiarios asignados a la fase
    phase_beneficiaries = Beneficiary.objects.filter(
        id__in=selected_beneficiary_ids,
        is_active=True
    ).order_by('first_name', 'last_name')

    context = {
        'project': project,
        'phase': phase,
        'all_beneficiaries': all_beneficiaries,
        'selected_beneficiary_ids': selected_beneficiary_ids,
        'phase_beneficiaries': phase_beneficiaries,
    }

    return render(request, 'dashboard/phase_edit.html', context)

@login_required
def phase_detail(request, project_id, phase_id):
    """
    Vista para ver el detalle de una fase con sus evidencias.
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence, PhaseBeneficiary, Beneficiary

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)

    # Obtener beneficiarios de la fase
    phase_beneficiaries = PhaseBeneficiary.objects.filter(phase=phase).select_related('beneficiary')

    # Obtener evidencias de la fase
    evidences = PhaseEvidence.objects.filter(phase=phase).order_by('-start_date', '-created_at')

    # Obtener todos los beneficiarios disponibles
    all_beneficiaries = Beneficiary.objects.filter(is_active=True).order_by('first_name', 'last_name')

    context = {
        'project': project,
        'phase': phase,
        'phase_beneficiaries': [pb.beneficiary for pb in phase_beneficiaries],
        'evidences': evidences,
        'all_beneficiaries': all_beneficiaries,
    }

    return render(request, 'dashboard/phase_detail.html', context)


@login_required
def phase_delete(request, project_id, phase_id):
    """
    Vista para eliminar una fase.
    """
    from django.http import JsonResponse
    from webAMG.models import Project, ProjectPhase

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)

    if request.method == 'POST':
        password = request.POST.get('password')

        if not password:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Debe ingresar su contraseña para confirmar la eliminación.'}, status=400)
            messages.error(request, 'Debe ingresar su contraseña para confirmar la eliminación.')
            return redirect('project_detail', project_id=project_id)

        if request.user.check_password(password):
            phase.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Fase "{phase.phase_name}" eliminada exitosamente.'})
            messages.success(request, f'Fase "{phase.phase_name}" eliminada exitosamente.')
            return redirect('project_detail', project_id=project_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Contraseña incorrecta.'}, status=400)
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('project_detail', project_id=project_id)

    return redirect('project_detail', project_id=project_id)


# =====================================================
# VISTAS PARA EVIDENCIAS DE FASES
# =====================================================

@login_required
def phase_evidence_add(request, project_id, phase_id):
    """
    Vista para agregar una evidencia a una fase.
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence, PhaseEvidencePhoto, PhaseEvidenceBeneficiary, Beneficiary

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)

    if request.method == 'POST':
        try:
            import os
            import time
            from django.conf import settings

            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')

            # Validar fechas
            if not start_date:
                messages.error(request, 'Debe especificar la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            # Si no se especifica fecha de fin, usar la fecha de inicio
            if not end_date:
                end_date = start_date

            if end_date < start_date:
                messages.error(request, 'La fecha de fin debe ser posterior o igual a la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            if not description:
                messages.error(request, 'Debe proporcionar una descripción de la evidencia.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            # Crear la evidencia
            evidence = PhaseEvidence.objects.create(
                phase=phase,
                start_date=start_date,
                end_date=end_date,
                description=description,
                created_by=request.user
            )

            # Actualizar SOLO el updated_at de la fase SIN afectar created_at
            phase.updated_at = timezone.now()
            phase.save(update_fields=['updated_at'])

            # Procesar beneficiarios
            beneficiaries_ids = request.POST.get('beneficiaries', '').split(',')
            beneficiaries_ids = [int(b_id.strip()) for b_id in beneficiaries_ids if b_id.strip().isdigit()]

            for beneficiary_id in beneficiaries_ids:
                try:
                    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                    PhaseEvidenceBeneficiary.objects.create(
                        phase_evidence=evidence,
                        beneficiary=beneficiary
                    )
                except Beneficiary.DoesNotExist:
                    pass

            # Procesar fotos
            photos = request.FILES.getlist('photos')

            if photos:
                # Crear directorio si no existe
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'Fases')
                os.makedirs(upload_dir, exist_ok=True)

                for i, photo in enumerate(photos, start=1):
                    # Generar nombre único para el archivo
                    file_extension = os.path.splitext(photo.name)[1]
                    unique_filename = f"phase_evidence_{phase.id}_{evidence.id}_{int(time.time())}_{i}{file_extension}"
                    file_path = os.path.join(upload_dir, unique_filename)

                    # Guardar el archivo
                    with open(file_path, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)

                    # Guardar la foto en la base de datos
                    PhaseEvidencePhoto.objects.create(
                        phase_evidence=evidence,
                        photo_url=os.path.join('Proyectos', 'Fases', unique_filename).replace('\\', '/'),
                        photo_order=i,
                        uploaded_by=request.user
                    )

            messages.success(request, f'Evidencia agregada exitosamente a la fase "{phase.phase_name}".')
            return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

        except Exception as e:
            messages.error(request, f'Error al agregar la evidencia: {str(e)}')

    return redirect('phase_detail', project_id=project_id, phase_id=phase_id)


@login_required
def phase_evidence_edit(request, project_id, phase_id, evidence_id):
    """
    Vista para editar una evidencia de una fase.
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence, PhaseEvidencePhoto, PhaseEvidenceBeneficiary, Beneficiary
    from django.utils import timezone

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)
    evidence = get_object_or_404(PhaseEvidence, id=evidence_id, phase=phase)

    if request.method == 'POST':
        try:
            import os
            import time
            from django.conf import settings

            print("DEBUG: Editando evidencia de fase")
            print(f"DEBUG: POST data keys: {list(request.POST.keys())}")
            print(f"DEBUG: beneficiaries: {request.POST.get('beneficiaries', 'NONE')}")
            print(f"DEBUG: photos_to_delete: {request.POST.getlist('photos_to_delete')}")
            print(f"DEBUG: photos count: {len(request.FILES.getlist('photos'))}")

            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')

            # Validar fechas
            if not start_date:
                messages.error(request, 'Debe especificar la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            if not end_date:
                end_date = start_date

            if end_date < start_date:
                messages.error(request, 'La fecha de fin debe ser posterior o igual a la fecha de inicio.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            if not description:
                messages.error(request, 'Debe proporcionar una descripción de la evidencia.')
                return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

            # Actualizar la evidencia
            evidence.start_date = start_date
            evidence.end_date = end_date
            evidence.description = description
            evidence.save()

            # Actualizar el updated_at de la fase
            phase.updated_at = timezone.now()
            phase.save(update_fields=['updated_at'])

            # Eliminar beneficiarios existentes y volver a agregarlos
            print(f"DEBUG: Eliminando beneficiarios existentes...")
            PhaseEvidenceBeneficiary.objects.filter(phase_evidence=evidence).delete()
            beneficiaries_ids = request.POST.get('beneficiaries', '').split(',')
            beneficiaries_ids = [int(b_id.strip()) for b_id in beneficiaries_ids if b_id.strip().isdigit()]
            print(f"DEBUG: Nuevos beneficiarios IDs: {beneficiaries_ids}")

            for beneficiary_id in beneficiaries_ids:
                try:
                    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                    PhaseEvidenceBeneficiary.objects.create(
                        phase_evidence=evidence,
                        beneficiary=beneficiary
                    )
                    print(f"DEBUG: Beneficiario {beneficiary_id} agregado")
                except Beneficiary.DoesNotExist:
                    print(f"DEBUG: Beneficiario {beneficiary_id} no encontrado")
                    pass

            # Procesar nuevas fotos
            photos = request.FILES.getlist('photos')
            print(f"DEBUG: Nuevas fotos: {len(photos)}")

            if photos:
                # Crear directorio si no existe
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'Fases')
                os.makedirs(upload_dir, exist_ok=True)

                # Obtener el último orden de foto
                last_order = PhaseEvidencePhoto.objects.filter(phase_evidence=evidence).order_by('-photo_order').first()
                start_order = (last_order.photo_order + 1) if last_order else 1

                for i, photo in enumerate(photos, start=start_order):
                    # Generar nombre único para el archivo
                    file_extension = os.path.splitext(photo.name)[1]
                    unique_filename = f"phase_evidence_{phase.id}_{evidence.id}_{int(time.time())}_{i}{file_extension}"
                    file_path = os.path.join(upload_dir, unique_filename)

                    # Guardar el archivo
                    with open(file_path, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)

                    # Guardar la foto en la base de datos
                    PhaseEvidencePhoto.objects.create(
                        phase_evidence=evidence,
                        photo_url=os.path.join('Proyectos', 'Fases', unique_filename).replace('\\', '/'),
                        photo_order=i,
                        uploaded_by=request.user
                    )
                    print(f"DEBUG: Nueva foto guardada: {unique_filename}")

            # Eliminar fotos marcadas para borrar
            photos_to_delete = request.POST.getlist('photos_to_delete')
            print(f"DEBUG: Fotos a eliminar: {photos_to_delete}")
            for photo_id in photos_to_delete:
                try:
                    photo = PhaseEvidencePhoto.objects.get(id=photo_id, phase_evidence=evidence)
                    # Eliminar el archivo físico
                    file_path = os.path.join(settings.MEDIA_ROOT, photo.photo_url)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"DEBUG: Archivo eliminado: {photo.photo_url}")
                    photo.delete()
                    print(f"DEBUG: Foto {photo_id} eliminada de la BD")
                except PhaseEvidencePhoto.DoesNotExist:
                    print(f"DEBUG: Foto {photo_id} no encontrada")
                    pass

            # Actualizar el orden de las fotos restantes
            remaining_photos = request.POST.getlist('photo_order')
            for i, photo_id in enumerate(remaining_photos, start=1):
                try:
                    photo = PhaseEvidencePhoto.objects.get(id=photo_id, phase_evidence=evidence)
                    photo.photo_order = i
                    photo.save()
                except PhaseEvidencePhoto.DoesNotExist:
                    pass

            messages.success(request, f'Evidencia actualizada exitosamente.')
            return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

        except Exception as e:
            print(f"DEBUG: Error al actualizar evidencia: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al actualizar la evidencia: {str(e)}')

    return redirect('phase_detail', project_id=project_id, phase_id=phase_id)


@login_required
def phase_evidence_delete(request, project_id, phase_id, evidence_id):
    """
    Vista para eliminar una evidencia de una fase.
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)
    evidence = get_object_or_404(PhaseEvidence, id=evidence_id, phase=phase)

    if request.method == 'POST':
        try:
            import os
            from django.conf import settings

            # Eliminar fotos físicas
            for photo in evidence.photos.all():
                file_path = os.path.join(settings.MEDIA_ROOT, photo.photo_url)
                if os.path.exists(file_path):
                    os.remove(file_path)

            evidence.delete()

            # Actualizar el updated_at de la fase
            phase.updated_at = timezone.now()
            phase.save(update_fields=['updated_at'])

            messages.success(request, 'Evidencia eliminada exitosamente.')
            return redirect('phase_detail', project_id=project_id, phase_id=phase_id)

        except Exception as e:
            messages.error(request, f'Error al eliminar la evidencia: {str(e)}')

    return redirect('phase_detail', project_id=project_id, phase_id=phase_id)


@login_required
def phase_evidence_photos(request, project_id, phase_id, evidence_id):
    """
    Vista para obtener las fotos de una evidencia de fase (JSON).
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)
    evidence = get_object_or_404(PhaseEvidence, id=evidence_id, phase=phase)

    photos = PhaseEvidencePhoto.objects.filter(phase_evidence=evidence).order_by('photo_order')

    photos_data = [
        {
            'id': photo.id,
            'photo_url': photo.photo_url,
            'caption': photo.caption,
            'photo_order': photo.photo_order
        }
        for photo in photos
    ]

    return JsonResponse({'photos': photos_data})


@login_required
def phase_evidence_beneficiaries(request, project_id, phase_id, evidence_id):
    """
    Vista para obtener los beneficiarios de una evidencia de fase (JSON).
    """
    from webAMG.models import Project, ProjectPhase, PhaseEvidence, PhaseEvidenceBeneficiary

    project = get_object_or_404(Project, id=project_id)
    phase = get_object_or_404(ProjectPhase, id=phase_id, project=project)
    evidence = get_object_or_404(PhaseEvidence, id=evidence_id, phase=phase)

    evidence_beneficiaries = PhaseEvidenceBeneficiary.objects.filter(phase_evidence=evidence).select_related('beneficiary')

    beneficiaries_data = [
        {
            'id': eb.beneficiary.id,
            'first_name': eb.beneficiary.first_name,
            'last_name': eb.beneficiary.last_name,
            'cui_dpi': eb.beneficiary.cui_dpi,
            'community': eb.beneficiary.community
        }
        for eb in evidence_beneficiaries
    ]

    return JsonResponse({'beneficiaries': beneficiaries_data})


# =====================================================
# VISTAS DE EVIDENCIAS DE PROYECTO (completar faltantes)
# =====================================================

@login_required
def project_evidence_edit(request, project_id, evidence_id):
    """
    Vista para editar una evidencia de proyecto.
    """
    from webAMG.models import Project, ProjectEvidence, EvidencePhoto, EvidenceBeneficiary, Beneficiary
    from datetime import datetime
    import os
    import time
    from django.conf import settings

    project = get_object_or_404(Project, id=project_id)
    evidence = get_object_or_404(ProjectEvidence, id=evidence_id, project=project)

    if request.method == 'POST':
        print("DEBUG: Editando evidencia de proyecto")
        print(f"DEBUG: POST data keys: {list(request.POST.keys())}")
        print(f"DEBUG: beneficiaries: {request.POST.get('beneficiaries', 'NONE')}")
        print(f"DEBUG: photos_to_delete: {request.POST.getlist('photos_to_delete')}")
        print(f"DEBUG: photos count: {len(request.FILES.getlist('photos'))}")

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        if start_date:
            evidence.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            evidence.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        if description:
            evidence.description = description

        evidence.save()

        # Eliminar beneficiarios existentes y volver a agregarlos
        print(f"DEBUG: Eliminando beneficiarios existentes...")
        EvidenceBeneficiary.objects.filter(evidence=evidence).delete()
        beneficiaries_ids = request.POST.get('beneficiaries', '').split(',')
        beneficiaries_ids = [int(b_id.strip()) for b_id in beneficiaries_ids if b_id.strip().isdigit()]
        print(f"DEBUG: Nuevos beneficiarios IDs: {beneficiaries_ids}")

        for beneficiary_id in beneficiaries_ids:
            try:
                beneficiary = Beneficiary.objects.get(id=beneficiary_id)
                EvidenceBeneficiary.objects.create(
                    evidence=evidence,
                    beneficiary=beneficiary
                )
                print(f"DEBUG: Beneficiario {beneficiary_id} agregado")
            except Beneficiary.DoesNotExist:
                print(f"DEBUG: Beneficiario {beneficiary_id} no encontrado")
                pass

        # Procesar nuevas fotos
        photos = request.FILES.getlist('photos')
        print(f"DEBUG: Nuevas fotos: {len(photos)}")

        if photos:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'Proyectos', 'Evidencias')
            os.makedirs(upload_dir, exist_ok=True)

            last_order = EvidencePhoto.objects.filter(evidence=evidence).order_by('-photo_order').first()
            start_order = (last_order.photo_order + 1) if last_order else 1

            for i, photo in enumerate(photos, start=start_order):
                file_extension = os.path.splitext(photo.name)[1]
                unique_filename = f"evidence_{project.id}_{evidence.id}_{int(time.time())}_{i}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)

                with open(file_path, 'wb+') as destination:
                    for chunk in photo.chunks():
                        destination.write(chunk)

                EvidencePhoto.objects.create(
                    evidence=evidence,
                    photo_url=os.path.join('Proyectos', 'Evidencias', unique_filename).replace('\\', '/'),
                    photo_order=i,
                    uploaded_by=request.user
                )
                print(f"DEBUG: Nueva foto guardada: {unique_filename}")

        # Eliminar fotos marcadas para borrar
        photos_to_delete = request.POST.getlist('photos_to_delete')
        print(f"DEBUG: Fotos a eliminar: {photos_to_delete}")
        for photo_id in photos_to_delete:
            try:
                photo = EvidencePhoto.objects.get(id=photo_id, evidence=evidence)
                file_path = os.path.join(settings.MEDIA_ROOT, photo.photo_url)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"DEBUG: Archivo eliminado: {photo.photo_url}")
                photo.delete()
                print(f"DEBUG: Foto {photo_id} eliminada de la BD")
            except EvidencePhoto.DoesNotExist:
                print(f"DEBUG: Foto {photo_id} no encontrada")
                pass

        messages.success(request, 'Evidencia actualizada exitosamente.')
        return redirect('project_detail', project_id=project_id)

    context = {
        'project': project,
        'evidence': evidence,
    }
    return render(request, 'dashboard/evidence_edit.html', context)


@login_required
def project_evidence_delete(request, project_id, evidence_id):
    """
    Vista para eliminar una evidencia de proyecto.
    """
    from django.http import JsonResponse
    from webAMG.models import Project, ProjectEvidence
    
    project = get_object_or_404(Project, id=project_id)
    evidence = get_object_or_404(ProjectEvidence, id=evidence_id, project=project)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            evidence.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Evidencia eliminada exitosamente.'})
            messages.success(request, 'Evidencia eliminada exitosamente.')
            return redirect('project_detail', project_id=project_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Contraseña incorrecta.'}, status=400)
            messages.error(request, 'Contraseña incorrecta.')
    
    context = {
        'project': project,
        'evidence': evidence,
    }
    return render(request, 'dashboard/evidence_delete.html', context)


@login_required
def project_evidence_photos(request, project_id, evidence_id):
    """
    Vista para obtener las fotos de una evidencia de proyecto (JSON).
    """
    from django.http import JsonResponse
    from webAMG.models import Project, ProjectEvidence, EvidencePhoto
    
    project = get_object_or_404(Project, id=project_id)
    evidence = get_object_or_404(ProjectEvidence, id=evidence_id, project=project)
    
    photos = EvidencePhoto.objects.filter(evidence=evidence).order_by('photo_order')
    
    photos_data = [
        {
            'id': photo.id,
            'photo_url': photo.photo_url,
            'caption': photo.caption,
            'photo_order': photo.photo_order
        }
        for photo in photos
    ]
    
    return JsonResponse({'photos': photos_data})


@login_required
def project_evidence_beneficiaries(request, project_id, evidence_id):
    """
    Vista para obtener los beneficiarios de una evidencia de proyecto (JSON).
    """
    from django.http import JsonResponse
    from webAMG.models import Project, ProjectEvidence, EvidenceBeneficiary
    
    project = get_object_or_404(Project, id=project_id)
    evidence = get_object_or_404(ProjectEvidence, id=evidence_id, project=project)
    
    evidence_beneficiaries = EvidenceBeneficiary.objects.filter(evidence=evidence).select_related('beneficiary')
    
    beneficiaries_data = [
        {
            'id': eb.beneficiary.id,
            'first_name': eb.beneficiary.first_name,
            'last_name': eb.beneficiary.last_name,
            'cui_dpi': eb.beneficiary.cui_dpi,
            'community': eb.beneficiary.community
        }
        for eb in evidence_beneficiaries
    ]
    
    return JsonResponse({'beneficiaries': beneficiaries_data})


@login_required
def project_timestamp_ajax(request, project_id):
    """
    Vista AJAX para obtener el timestamp del proyecto.
    """
    from django.http import JsonResponse
    from webAMG.models import Project
    
    project = get_object_or_404(Project, id=project_id)
    
    return JsonResponse({
        'created_at': project.created_at.isoformat() if project.created_at else None,
        'updated_at': project.updated_at.isoformat() if project.updated_at else None,
    })


# =====================================================
# VISTAS DE PRUEBA
# =====================================================

def test_timezone_view(request):
    """
    Vista de prueba para verificar la configuración de zona horaria.
    """
    from django.utils import timezone
    
    context = {
        'current_time': timezone.now(),
        'timezone': timezone.get_current_timezone(),
        'settings_timezone': timezone.get_current_timezone_name(),
    }
    return render(request, 'test_timezone.html', context)


# =====================================================
# VISTAS PÚBLICAS
# =====================================================

def about(request):
    """
    Vista de la página 'Acerca de'.
    """
    return render(request, 'about.html')


def contact(request):
    """
    Vista de la página de contacto.
    """
    return render(request, 'contact.html')

