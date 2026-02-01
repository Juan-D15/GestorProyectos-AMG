"""
Vistas para renderizar páginas HTML de la aplicación.
Este módulo contiene todas las vistas que renderizan plantillas HTML.
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
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
def project_create_page(request):
    """Vista de la página de creación de proyectos."""
    return render(request, "dashboard/project_create.html", {'user': request.user})


@login_required
def beneficiaries_page(request):
    """Vista de la sección Beneficiarios."""
    return render(request, "dashboard/beneficiaries.html", {'user': request.user})


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
