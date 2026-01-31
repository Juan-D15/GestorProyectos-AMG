"""
URL configuration para el proyecto WebAMG.
"""
from django.contrib import admin
from django.urls import path, include
from webAMG import views_pages
from webAMG import views as api_views


urlpatterns = [
    # Paginas de autenticacion
    path("", views_pages.login_page, name="home"),
    path("login/", views_pages.login_page, name="login"),
    
    # Paginas publicas (sin autenticacion)
    path("about/", views_pages.about, name="about"),
    path("contact/", views_pages.contact, name="contact"),
    path("logout/", views_pages.logout_page, name="logout"),
    
    # Paginas del Dashboard (requieren autenticacion)
    path("dashboard/", views_pages.dashboard, name="dashboard"),
    path("dashboard/proyectos/", views_pages.projects_page, name="dashboard_projects"),
    path("dashboard/beneficiarios/", views_pages.beneficiaries_page, name="dashboard_beneficiaries"),
    path("dashboard/presupuesto/", views_pages.budget_page, name="dashboard_budget"),
    path("dashboard/reportes/", views_pages.reports_page, name="dashboard_reports"),
    path("dashboard/estadisticas/", views_pages.statistics_page, name="dashboard_statistics"),
    path("dashboard/perfil/", views_pages.profile_page, name="dashboard_profile"),
    
    # Gestion de Usuarios (solo administradores)
    path("dashboard/usuarios/", views_pages.dashboard_users, name="dashboard_users"),
    path("dashboard/usuarios/crear/", views_pages.user_create, name="user_create"),
    path("dashboard/usuarios/editar/<int:user_id>/", views_pages.user_edit, name="user_edit"),
    path("dashboard/usuarios/eliminar/", views_pages.user_delete, name="user_delete"),
    
    # Django Admin
    path("admin/", admin.site.urls),
    
    # ReactPy-Django WebSocket routes
    path("reactpy/", include("reactpy_django.http.urls")),
]
