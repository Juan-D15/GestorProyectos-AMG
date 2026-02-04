"""
URL configuration para el proyecto WebAMG.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
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
]

# Media files (User uploaded files) - Solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
