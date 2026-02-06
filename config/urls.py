"""
URL configuration para el proyecto WebAMG.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from webAMG import views_pages
from webAMG import views as api_views
from webAMG.api import v1 as api_v1


urlpatterns = [
    # Paginas de autenticacion
    path("", views_pages.login_page, name="home"),
    path("login/", views_pages.login_page, name="login"),
    
    # Paginas publicas (sin autenticacion)
    path("about/", views_pages.about, name="about"),
    path("contact/", views_pages.contact, name="contact"),
    path("logout/", views_pages.logout_page, name="logout"),
    path("test-timezone/", views_pages.test_timezone_view, name="test_timezone"),
    
    # Paginas del Dashboard (requieren autenticacion)
    path("dashboard/", views_pages.dashboard, name="dashboard"),
    path("dashboard/proyectos/", views_pages.project_list_page, name="dashboard_projects"),
    path("dashboard/proyectos/lista/", views_pages.project_list_page, name="project_list"),
    path("dashboard/proyectos/crear/", views_pages.project_create_page, name="project_create"),
    path("dashboard/proyectos/<int:project_id>/", views_pages.project_detail_page, name="project_detail"),
    path("dashboard/proyectos/<int:project_id>/editar/", views_pages.project_edit_page, name="project_edit"),
    path("dashboard/proyectos/<int:project_id>/eliminar/", views_pages.project_delete_page, name="project_delete"),
    path("dashboard/proyectos/<int:project_id>/evidencias/agregar/", views_pages.project_evidence_add, name="project_evidence_add"),
    path("dashboard/proyectos/<int:project_id>/evidencias/<int:evidence_id>/editar/", views_pages.project_evidence_edit, name="project_evidence_edit"),
    path("dashboard/proyectos/<int:project_id>/evidencias/<int:evidence_id>/eliminar/", views_pages.project_evidence_delete, name="project_evidence_delete"),
    path("dashboard/proyectos/<int:project_id>/evidencias/<int:evidence_id>/fotos/", views_pages.project_evidence_photos, name="project_evidence_photos"),
    path("dashboard/proyectos/<int:project_id>/evidencias/<int:evidence_id>/beneficiarios/", views_pages.project_evidence_beneficiaries, name="project_evidence_beneficiaries"),
    path("dashboard/proyectos/<int:project_id>/timestamp/", views_pages.project_timestamp_ajax, name="project_timestamp_ajax"),

    # Fases de proyectos
    path("dashboard/proyectos/<int:project_id>/fases/crear/", views_pages.phase_create, name="phase_create"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/", views_pages.phase_detail, name="phase_detail"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/editar/", views_pages.phase_edit, name="phase_edit"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/eliminar/", views_pages.phase_delete, name="phase_delete"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/evidencias/agregar/", views_pages.phase_evidence_add, name="phase_evidence_add"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/evidencias/<int:evidence_id>/editar/", views_pages.phase_evidence_edit, name="phase_evidence_edit"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/evidencias/<int:evidence_id>/eliminar/", views_pages.phase_evidence_delete, name="phase_evidence_delete"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/evidencias/<int:evidence_id>/fotos/", views_pages.phase_evidence_photos, name="phase_evidence_photos"),
    path("dashboard/proyectos/<int:project_id>/fases/<int:phase_id>/evidencias/<int:evidence_id>/beneficiarios/", views_pages.phase_evidence_beneficiaries, name="phase_evidence_beneficiaries"),

    path("dashboard/beneficiarios/", views_pages.beneficiaries_page, name="dashboard_beneficiaries"),
    path("dashboard/presupuesto/", views_pages.budget_page, name="dashboard_budget"),
    path("dashboard/reportes/", views_pages.reports_page, name="dashboard_reports"),
    path("dashboard/estadisticas/", views_pages.statistics_page, name="dashboard_statistics"),
    path("dashboard/perfil/", views_pages.profile_page, name="dashboard_profile"),
    
    # Gestion de Usuarios (solo administradores)
    path("dashboard/usuarios/", views_pages.dashboard_users, name="dashboard_users"),
    path("dashboard/usuarios/crear/", views_pages.user_create, name="user_create"),
    path("dashboard/usuarios/editar/", views_pages.user_edit, name="user_edit"),
    path("dashboard/usuarios/eliminar/", views_pages.user_delete, name="user_delete"),
    
    # Django Admin
    path("admin/", admin.site.urls),
    
    # ReactPy-Django WebSocket routes
    path("reactpy/", include("reactpy_django.http.urls")),
    
    # API v1 - Endpoints versionados y seguros
    path("api/v1/health/", api_v1.health_check, name="api_v1_health"),
    path("api/v1/info/", api_v1.api_info, name="api_v1_info"),
    path("api/v1/auth/login/", api_v1.login, name="api_v1_login"),
    path("api/v1/auth/logout/", api_v1.logout, name="api_v1_logout"),
    path("api/v1/auth/verify/", api_v1.verify_session, name="api_v1_verify"),
    path("api/v1/auth/me/", api_v1.current_user, name="api_v1_current_user"),
    path("api/v1/users/", api_v1.list_users, name="api_v1_list_users"),
    path("api/v1/users/create/", api_v1.create_user, name="api_v1_create_user"),
    path("api/v1/users/<int:user_id>/", api_v1.user_detail, name="api_v1_user_detail"),
    path("api/v1/users/<int:user_id>/update/", api_v1.update_user, name="api_v1_update_user"),
    path("api/v1/users/<int:user_id>/delete/", api_v1.delete_user, name="api_v1_delete_user"),
    # Proyectos - Soft delete
    path("api/v1/projects/<int:project_id>/deactivate/", api_v1.deactivate_project, name="api_v1_deactivate_project"),
    path("api/v1/projects/<int:project_id>/activate/", api_v1.activate_project, name="api_v1_activate_project"),
]

# Media files (User uploaded files) - Solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
