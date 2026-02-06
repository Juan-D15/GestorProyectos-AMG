# AGENTS.md - Guide for Coding Agents

## Build / Test Commands

### Environment Setup
- Activate venv: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)

### CSS
- `npm run build:css` - Compile TailwindCSS with DaisyUI
- `npm run watch:css` - Watch mode for CSS development

### Django
- `python manage.py runserver` - Start dev server (http://localhost:8000)
- `python manage.py migrate` - Apply migrations
- `python manage.py makemigrations` - Create migrations
- `python manage.py collectstatic` - Collect static files (production)
- `python manage.py create_admin` - Create default admin user
- `python manage.py check_timezone` - Verify Django/PostgreSQL timezone configuration

### Testing
- `python manage.py test` - Run all tests
- `python manage.py test webAMG.tests.TestCaseName` - Run specific test class
- `python manage.py test webAMG.tests.TestCaseName.test_method` - Run single test method
- `python manage.py test webAMG.tests_timezone` - Run timezone-specific tests
- Use `--verbosity=2` for detailed output, `--keepdb` to preserve database between runs

### Production
- `daphne config.asgi:application` - Run production server with ReactPy
- Set `DEBUG=False` in .env for production
- Use `ALLOWED_HOSTS` environment variable for allowed domains

### Linting/Type Checking (if configured)
- No linter currently configured (no .flake8, .pylintrc, or .ruff.toml found)
- No type checker currently configured (no mypy.ini or pyproject.toml with mypy settings)
- Follow PEP 8 manually for Python code formatting

## Code Style Guidelines

### Python
- **Naming**: snake_case for vars/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants
- **Imports**: Standard library → third-party → local (with blank lines between each group)
- **Docstrings**: Google-style with Args/Returns/Raises sections, module-level docstrings required
- **Type hints**: Required for all function parameters and returns (e.g., `def login(username: str) -> dict:`)
- **Error handling**: Specific exceptions, return `{'success': False, 'error': 'msg'}` for APIs, use Django messages for UI
- **Formatting**: No formatter configured, follow PEP 8 conventions manually

### Django Patterns
- **Models**: Use custom User (`AUTH_USER_MODEL = 'webAMG.User'`), add `db_column` for foreign keys, use `TextField` for long text, add Meta class with verbose_name/db_table/indexes, define `__str__()`, use model choices enums
- **Views**: Separate `views.py` (APIs/JSON) and `views_pages.py` (HTML), use decorators: `@login_required`, `@require_http_methods`, `@csrf_exempt`, use Django messages, redirect using named URLs, use `get_object_or_404` for details, API views return `JsonResponse` with proper status codes (200, 400, 401, 500)
- **Authentication**: Django built-in, custom backend `webAMG.authentication.CustomUserBackend`, check role: `user.role == 'administrador'` or `user.is_admin()`
- **Forms**: Inherit from Django forms, add TailwindCSS classes in `__init__`
- **Timezone**: Always use `django.utils.timezone.now()` instead of `datetime.now()`
- **Settings**: Use environment variables via `os.environ.get()` or `python-dotenv`, TIME_ZONE = 'America/Guatemala'
- **Database**: PostgreSQL with psycopg2-binary, always use raw SQL scripts for schema changes before updating models

### ReactPy
- **Naming**: snake_case for components
- **Registration**: Register full module path in settings.py REACTPY_REGISTERED_COMPONENTS
- **Structure**: `@component` decorator, return `html.div()` etc., use `hooks.use_state()` for state
- **Colors**: Use color_map dict: `{'primary': '#8a4534', 'secondary': '#07680b', 'accent': '#334e76'}`
- **Args**: Use inline type hints in component signature (e.g., `title: str, value: str`)
- **State**: Always use `hooks.use_state()` for interactive components, pass callbacks as lambda functions

### HTML/Templates
- Use TailwindCSS, extend base templates, `{% load static %}`, `{% csrf_token %}`
- Forms: POST for actions, GET for navigation, display `form.errors`
- Include fonts: Inter (Google Fonts), Font Awesome (icons)
- Use `{{ form.field }}` for Django form fields with error handling

### Environment Variables
- Store in `.env` (never commit this file)
- Access via `os.environ.get('VARIABLE_NAME')` or `python-dotenv`
- Required: `KEY_DJANGO`, `DEBUG`, `ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- Reference `.env.example` for required variables

## Database Schema & Changes

### Schema Reference
- **Database definition**: `BasedeDatos.txt` (PostgreSQL schema with tables, indexes, triggers, views)
- **Stored procedures**: `ProcedimientosAlmacenados-DB.txt` (PL/pgSQL functions for projects, beneficiaries, evidence, budget)
- **Table names**: Plural snake_case matching PostgreSQL schema (e.g., `users`, `beneficiaries`, `projects`)
- **Foreign keys**: Always use `db_column` parameter to match PostgreSQL schema (e.g., `db_column='user_id'`)

### Making Database Changes
When database schema changes are required:
1. Create SQL migration script at project root: `migration_YYYYMMDD_descripcion.sql`
2. Script should contain `ALTER TABLE`, `CREATE INDEX`, `CREATE FUNCTION`, etc.
3. Apply manually to PostgreSQL: `psql -U username -d database -f migration_YYYYMMDD_descripcion.sql`
4. After applying, update Django models to match new schema
5. Run `python manage.py makemigrations --empty` if needed for Django sync
6. Test thoroughly before committing

## Project Structure
```
webAMG/
├── api/          - API endpoints
├── core/         - ReactPy components
├── services/     - Business logic (auth_service.py)
├── templates/    - HTML templates
├── static/       - CSS/JS (src/ source, dist/ compiled)
│   └── src/
│       ├── js/   - Create new files for new features
│       └── css/  - Create new files for new styles
├── templatetags/ - Custom template tags
├── models.py     - Database models (match PostgreSQL schema)
├── views.py      - API views (JSON)
├── views_pages.py - Page views (HTML)
├── forms.py      - Django forms
├── authentication.py - Custom auth backend
└── tests.py      - Django tests
config/
└── settings.py   - Django settings
```

## Best Practices

**Security**: Never commit .env, validate all input, CSRF enabled, @login_required for protected views, check user roles before sensitive operations

**Sessions**: 8-hour expiry, use Django's session framework, clean expired with `AuthService.clean_expired_sessions()`

**Testing**: Tests in `webAMG/tests.py`, use Django TestCase, mock dependencies, test both success and error cases

**Code Quality**: Keep functions under 50 lines, use meaningful names, follow Django REST conventions, comment complex logic

**HTTP Status Codes**: 200 (success), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)

**Corporate Colors**: Primary (#8a4534) for main buttons, Secondary (#07680b) for alerts, Accent (#334e76) for info UI

**API Response Format**: Always return `{'success': bool, 'message': str, 'data': dict}` for successful operations, `{'success': False, 'error': str}` for errors

**File Creation**: New CSS/JS files go in `webAMG/static/src/css/` or `webAMG/static/src/js/`, always run `npm run build:css` after CSS changes

**Error Handling Patterns**:
- API views: Wrap in try/except, return `JsonResponse({'success': False, 'error': str}, status=400/500)`
- Page views: Use Django messages framework with `messages.error(request, 'msg')` or `messages.success(request, 'msg')`
- Model operations: Use `get_object_or_404()` for retrieving single objects

**Commit Guidelines**:
- Never commit `.env`, `.venv/`, `__pycache__/`, `*.pyc`, `node_modules/`, `static/dist/`
- Run `python manage.py test` before committing if tests exist
- Migrate database changes with SQL scripts first, then update models

## API Security & Standards

### New API Structure
- **Versioned APIs**: Always use `/api/v1/...` for new endpoints (see `webAMG/api/v1.py`)
- **Legacy APIs**: Existing `/api/...` endpoints maintained for compatibility
- **Use New APIs**: All new endpoints should follow v1 patterns

### API Decorators (from `webAMG/api/decorators.py`)
- `@api_endpoint(methods=['GET','POST'], auth_required=True, roles={'admin'})` - Combined decorator
- `@api_require_auth` - Requires valid session token
- `@api_require_roles({'administrador'})` - Requires specific roles
- `@api_require_admin` - Shortcut for admin role
- `@handle_api_errors` - Consistent error handling (auto-applied by @api_endpoint)

### API Validators (from `webAMG/api/validators.py`)
- Use Pydantic models for request validation: `LoginRequest`, `CreateUserRequest`, etc.
- Use `validate_request_data(data, ModelClass)` for validation
- Use `APIResponse.success(data, message)` for success responses
- Use `APIResponse.error(error_code, message, details)` for error responses

### API Security Features
- **Rate Limiting**: Use `RateLimiter.check_rate_limit(id, endpoint, limit, window)` for brute-force protection
- **Input Sanitization**: Use `InputSanitizer.sanitize_string()`, `.sanitize_email()`, etc.
- **Security Headers**: Automatically applied by `SecurityHeadersMiddleware`
- **Structured Errors**: Use exceptions from `webAMG/api/exceptions.py` (BadRequestError, UnauthorizedError, etc.)

### Creating New API Endpoints
1. Create endpoint in `webAMG/api/v1.py`
2. Use `@api_endpoint` decorator with appropriate settings
3. Validate inputs with Pydantic models
4. Return consistent responses with `APIResponse`
5. Add URL in `config/urls.py` under `/api/v1/` prefix
6. Document in `API_SECURITY.md`

### Example API Endpoint
```python
@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def create_user(request):
    data = json.loads(request.body)
    validated = validate_request_data(data, CreateUserRequest)
    # ... create user logic ...
    return JsonResponse(APIResponse.success(
        data={'user': user_data},
        message='Usuario creado exitosamente'
    ))
```
