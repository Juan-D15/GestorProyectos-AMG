# WebAMG - Sistema de Gestión de Proyectos Maya Guatemala

Proyecto web construido con Django 6.0, TailwindCSS 4.1.18, DaisyUI 5.5.14 y ReactPy-Django.

## Tecnologías

- **Django 6.0.1** - Framework web de Python
- **TailwindCSS 4.1.18** - Framework de CSS utilitario
- **DaisyUI 5.5.14** - Componentes de UI para TailwindCSS
- **ReactPy-Django 1.0.0** - Integración de ReactPy con Django
- **PostgreSQL** - Base de datos

## Características

- ✅ Sistema de autenticación Django con roles (Administrador/Usuario)
- ✅ Dashboard con estadísticas y métricas
- ✅ Gestión de proyectos
- ✅ Gestión de beneficiarios
- ✅ Ejecución presupuestaria
- ✅ Reportes y estadísticas
- ✅ Diseño minimalista con colores corporativos
- ✅ Componentes ReactPy reutilizables
- ✅ Plantillas Django sin JavaScript (renderizado en servidor)
- ✅ Estructura de carpetas organizada y escalable

## Colores Corporativos

| Color | HEX | Uso |
|--------|------|------|
| Verde Primario | `#07680b` | Botones principales, enlaces activos |
| Marrón Secundario | `#8a4534` | Alertas, acciones secundarias |
| Azul Acento | `#334e76` | Información, elementos de UI |

## Requisitos Previos

- Python 3.11 o superior
- Node.js 18 o superior
- PostgreSQL 14 o superior

## Instalación

### 1. Clonar el repositorio y configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source .venv/bin/activate
```

### 2. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 3. Instalar dependencias de Node.js

```bash
npm install
```

### 4. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tu configuración
```

Variables de entorno requeridas:

```env
# Django Configuration
KEY_DJANGO=django-insecure-change-this-in-production-use-a-secure-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database Configuration
DB_NAME=webamg_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432
```

### 5. Crear base de datos PostgreSQL

```sql
CREATE DATABASE webamg_db;
```

### 6. Ejecutar migraciones de Django

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear usuario administrador por defecto

```bash
python manage.py create_admin
```

### 8. Compilar CSS con Tailwind

```bash
npm run build:css
```

Para desarrollo con modo watch:

```bash
npm run watch:css
```

## Ejecutar el Proyecto

### Modo Desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en `http://localhost:8000`

### Modo Producción con ASGI

```bash
daphne config.asgi:application
```

## Estructura del Proyecto

```
ProyectoWebAMG/
├── config/                  # Configuración de Django
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs del proyecto
│   ├── asgi.py              # Configuración ASGI (para ReactPy)
│   └── wsgi.py              # Configuración WSGI
├── webAMG/                  # Aplicación principal
│   ├── api/                 # Módulo para APIs y endpoints
│   │   └── __init__.py
│   ├── core/                # Módulo core (componentes, configuración)
│   │   ├── __init__.py
│   │   └── components.py    # Componentes de ReactPy
│   ├── utils/               # Módulo de utilidades y helpers
│   │   └── __init__.py
│   ├── services/            # Módulo de servicios y lógica de negocio
│   │   ├── __init__.py
│   │   └── auth_service.py  # Servicio de autenticación
│   ├── templates/           # Plantillas HTML
│   │   ├── auth/             # Plantillas de autenticación
│   │   │   └── login.html
│   │   ├── dashboard/        # Plantillas del dashboard
│   │   │   └── index.html
│   │   ├── base.html        # Plantilla base (reutilizable)
│   │   └── index.html       # Página principal (ReactPy demo)
│   ├── static/              # Archivos estáticos
│   │   ├── src/             # Fuentes CSS/JS
│   │   │   └── css/
│   │   │       └── styles.css
│   │   └── dist/            # CSS compilado (generado por Tailwind)
│   │       └── css/
│   │           └── styles.css
│   ├── views.py             # Vistas para APIs (JSON)
│   ├── views_pages.py       # Vistas para páginas HTML
│   ├── models.py            # Modelos de base de datos
│   ├── forms.py             # Formularios de Django
│   ├── management/          # Comandos de gestión
│   │   ├── commands/
│   │   │   └── create_admin.py
│   ├── admin.py             # Configuración de admin
│   ├── apps.py             # Configuración de la app
│   └── migrations/          # Migraciones de base de datos
├── requirements.txt         # Dependencias de Python
├── package.json             # Dependencias de Node.js
├── tailwind.config.js       # Configuración de Tailwind
├── .env.example             # Ejemplo de variables de entorno
└── manage.py                # Script de gestión de Django
```

## Arquitectura del Proyecto

### Separación de Responsabilidades

| Archivo | Propósito |
|---------|-----------|
| [`webAMG/views.py`](webAMG/views.py) | APIs y endpoints que devuelven JSON |
| [`webAMG/views_pages.py`](webAMG/views_pages.py) | Vistas que renderizan plantillas HTML |
| [`webAMG/core/components.py`](webAMG/core/components.py) | Componentes de ReactPy |
| [`webAMG/forms.py`](webAMG/forms.py) | Formularios de Django |
| [`webAMG/services/auth_service.py`](webAMG/services/auth_service.py) | Lógica de autenticación |
| `webAMG/api/` | Módulos para organizar APIs complejas |
| `webAMG/utils/` | Funciones de utilidad y helpers |
| `webAMG/services/` | Lógica de negocio y servicios externos |

## Sistema de Autenticación

El sistema utiliza el sistema de autenticación integrado de Django, que es más seguro y fácil de mantener.

### Roles de Usuario

El sistema cuenta con dos roles de usuario:

| Rol | Permisos |
|------|-----------|
| Administrador | Acceso completo a todas las funcionalidades |
| Usuario | Acceso limitado a visualización y edición básica |

### Autenticación Django

El sistema usa Django's built-in authentication system:

- **Login**: [`/login/`](login/) - Página de inicio de sesión
- **Logout**: [`/logout/`](logout/) - Cerrar sesión
- **Protección de vistas**: Decorador `@login_required` en vistas que requieren autenticación
- **Permisos**: Sistema de permisos integrado de Django para controlar acceso por rol

### Formulario de Login

El formulario de login usa Django's [`AuthenticationForm`](webAMG/forms.py) con validación integrada.

### Mensajes de Django

El sistema usa el framework de mensajes de Django para mostrar notificaciones (éxito, error, información).

## Endpoints Disponibles

### Páginas HTML

#### Páginas Públicas (sin autenticación)
- `GET /` - Página principal (ReactPy demo)
- `GET /about/` - Página "Acerca de"
- `GET /contact/` - Página de contacto

#### Páginas de Autenticación
- `GET /login/` - Página de login
- `GET /logout/` - Cerrar sesión

#### Páginas del Dashboard (requieren autenticación)
- `GET /dashboard/` - Dashboard principal
- `GET /dashboard/proyectos/` - Sección Proyectos
- `GET /dashboard/beneficiarios/` - Sección Beneficiarios
- `GET /dashboard/presupuesto/` - Sección Ejecución Presupuestaria
- `GET /dashboard/reportes/` - Sección Reportes
- `GET /dashboard/estadisticas/` - Sección Estadísticas
- `GET /dashboard/perfil/` - Perfil de usuario

### APIs
- `GET /api/health/` - Verificación de salud
- `GET /api/info/` - Información de la API

### Django Admin
- `/admin/` - Panel de administración

## Componentes de ReactPy

### Componentes de Prueba

- **simple**: Componente simple que muestra "HELLO FROM REACTPY"
- **hello_world**: Componente de saludo con parámetro
- **counter**: Componente contador interactivo con estado
- **test_component**: Componente de prueba básico

## Scripts Disponibles

### Node.js

- `npm run build:css` - Compila CSS con Tailwind
- `npm run watch:css` - Compila CSS en modo watch

### Django

- `python manage.py runserver` - Inicia servidor de desarrollo
- `python manage.py migrate` - Ejecuta migraciones
- `python manage.py makemigrations` - Crea nuevas migraciones
- `python manage.py createsuperuser` - Crea superusuario
- `python manage.py create_admin` - Crea usuario administrador por defecto
- `python manage.py collectstatic` - Recolecta archivos estáticos (producción)

## Notas Importantes

1. **DaisyUI v5 con Tailwind v4**: DaisyUI v5 está en beta para Tailwind v4. Si encuentras problemas, considera usar DaisyUI v4 con Tailwind v3.

2. **Base de datos PostgreSQL**: Asegúrate de que PostgreSQL esté corriendo y que las credenciales en `.env` sean correctas.

3. **CSS compilado**: Antes de ejecutar el proyecto, asegúrate de compilar el CSS con `npm run build:css`.

4. **Variables de entorno**: Nunca subas el archivo `.env` al repositorio. Usa `.env.example` como plantilla.

5. **Escalabilidad**: La estructura del proyecto está diseñada para crecer. Agrega nuevas funcionalidades en los módulos correspondientes según la arquitectura definida.

6. **Sesiones**: Las sesiones se manejan automáticamente por Django.

## Solución de Problemas

### Error de conexión a PostgreSQL

Verifica que:
- PostgreSQL esté corriendo
- Las credenciales en `.env` sean correctas
- La base de datos exista

### Error de componentes de ReactPy

Verifica que:
- `reactpy-django` esté instalado
- Los componentes estén registrados en `settings.py`
- El servidor ASGI esté configurado correctamente
- Los paths en las plantillas sean correctos (`webAMG.core.components.xxx`)

### CSS no se aplica

Verifica que:
- Hayas ejecutado `npm run build:css`
- El archivo `webAMG/static/dist/css/styles.css` exista
- La ruta en `base.html` sea correcta

### Error de autenticación

Verifica que:
- Las credenciales sean correctas
- El usuario esté activo en la base de datos (`is_active=True`)
- Las sesiones estén configuradas correctamente en settings

## Guía para Agregar Nuevas Funcionalidades

### Agregar una nueva página HTML protegida

1. Crea la plantilla en `webAMG/templates/`
2. Agrega la vista en `webAMG/views_pages.py` con el decorador `@login_required`
3. Agrega la URL en `config/urls.py`

```python
from django.contrib.auth.decorators import login_required

@login_required
def mi_nueva_pagina(request):
    return render(request, "mi_nueva_pagina.html", {'user': request.user})
```

### Agregar una página solo para administradores

```python
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_admin())
def pagina_admin(request):
    return render(request, "admin_page.html")
```

### Agregar un nuevo componente ReactPy

1. Crea el componente en `webAMG/core/components.py`
2. Regístralo en `config/settings.py` en `REACTPY_REGISTERED_COMPONENTS`
3. Úsalo en cualquier plantilla con `{% component "webAMG.core.components.nombre_componente" %}`

### Agregar un nuevo servicio

1. Crea el módulo en `webAMG/services/`
2. Importa y usa el servicio donde lo necesites

## Licencia

Este proyecto es de uso educativo.
