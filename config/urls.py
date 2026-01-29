from django.contrib import admin
from django.urls import path
from webAMG import views

urlpatterns = [
    path('', views.tailwind_test, name='home'),
    path('admin/', admin.site.urls),
    path('tailwind-test/', views.tailwind_test, name='tailwind_test'),
    path('daisyui-test/', views.daisyui_test, name='daisyui_test'),
]
