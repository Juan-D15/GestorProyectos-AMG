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
from .forms import LoginForm


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
    from webAMG.models import Project, ProjectBeneficiary, Beneficiary
    
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
    
    context = {
        'user': request.user,
        'project': project,
        'project_beneficiaries': beneficiaries,
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
            project.municipality = request.POST.get('municipality') or project.municipality
            project.department = request.POST.get('department') or project.department
            project.status = request.POST.get('status', project.status)
            project.has_phases = request.POST.get('has_phases') == 'on'
            project.progress_percentage = request.POST.get('progress_percentage', 0) or project.progress_percentage
            
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
    """
    from webAMG.models import Project
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        try:
            project_name = project.project_name
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
# EJEMPLO DE VISTAS ADICIONALES
# =====================================================

def about(request):
    """
    Vista de la página 'Acerca de'.
    """
    return render(request, "about.html")


def contact(request):
    """
    Vista de la página de contacto.
    """
    return render(request, "contact.html")


class AboutView(TemplateView):
    """Vista de la página 'Acerca de' (versión basada en clase)."""
    template_name = "about.html"


class ContactView(TemplateView):
    """Vista de la página de contacto (versión basada en clase)."""
    template_name = "contact.html"
