# API WebAMG v1 - Documentación de Seguridad

## 📋 Resumen de Mejoras de Seguridad

Este documento describe las mejoras de seguridad implementadas en las APIs del sistema WebAMG para cumplir con los estándares de seguridad y mejores prácticas de la industria.

## 🚀 Novedades

### 1. Versionamiento de API
- Estructura de URLs: `/api/v1/...`
- Facilita migraciones futuras sin romper clientes existentes
- Plan de deprecación de endpoints

### 2. Decoradores de Seguridad

#### `@api_require_auth`
Requiere autenticación válida (token de sesión).
```python
@api_require_auth
def protected_endpoint(request):
    return JsonResponse({'success': True})
```

#### `@api_require_roles({'administrador'})`
Requiere roles específicos.
```python
@api_require_auth
@api_require_roles({'administrador'})
def admin_only(request):
    return JsonResponse({'success': True})
```

#### `@api_require_admin`
Atajo para requerir rol de administrador.
```python
@api_require_admin
def sensitive_operation(request):
    return JsonResponse({'success': True})
```

#### `@api_endpoint` (decorador combinado)
Simplifica la aplicación de múltiples decoradores.
```python
@api_endpoint(
    methods=['GET', 'POST'],
    auth_required=True,
    roles={'administrador'}
)
def endpoint(request):
    return JsonResponse({'success': True})
```

### 3. Validación Robusta con Pydantic

#### Modelos de Request
```python
from webAMG.api.validators import LoginRequest

validated = validate_request_data(data, LoginRequest)
# username: 3-50 caracteres
# password: min 8 caracteres
```

#### Modelos de Response
```python
from webAMG.api.validators import APIResponse

return JsonResponse(
    APIResponse.success(
        data={'user': user_data},
        message='Usuario creado'
    )
)
```

### 4. Rate Limiting
Prevención de ataques de fuerza bruta y DoS.

```python
from webAMG.api.security import RateLimiter

RateLimiter.check_rate_limit(
    f"login_{username}",
    'login',
    limit=5,
    window=300  # 5 minutos
)
```

**Endpoints con Rate Limiting:**
- `POST /api/v1/auth/login/`: 5 intentos por 5 minutos

### 5. Sanitización de Input
Prevención de XSS, SQL Injection y otros ataques.

```python
from webAMG.api.security import InputSanitizer

clean_string = InputSanitizer.sanitize_string(user_input)
clean_email = InputSanitizer.sanitize_email(email_input)
clean_phone = InputSanitizer.sanitize_phone(phone_input)
```

### 6. Headers de Seguridad
Headers HTTP agregados automáticamente por middleware:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; ...
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=(), ...
```

### 7. Excepciones Estructuradas
Errores consistentes con códigos y detalles.

```python
from webAMG.api.exceptions import NotFoundError

raise NotFoundError(
    "Usuario no encontrado",
    error_code="USER_NOT_FOUND",
    details={'user_id': 123}
)
```

**Códigos de Error Disponibles:**
- `BAD_REQUEST` - 400
- `UNAUTHORIZED` - 401
- `FORBIDDEN` - 403
- `NOT_FOUND` - 404
- `CONFLICT` - 409
- `VALIDATION_ERROR` - 422
- `RATE_LIMIT_EXCEEDED` - 429
- `INTERNAL_ERROR` - 500

### 8. Logging de Requests
Middleware que registra todas las requests con:
- Método HTTP
- Path
- Status Code
- Duración
- IP del cliente
- User Agent
- ID de usuario (si está autenticado)

## 🔐 Endpoints de API v1

### Autenticación

#### `POST /api/v1/auth/login/`
Inicia sesión con rate limiting.

**Request:**
```json
{
  "username": "admin",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin User",
      "role": "administrador"
    },
    "expires_at": "2026-02-06T10:00:00Z"
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

**Rate Limit:** 5 intentos por 5 minutos por username.

#### `POST /api/v1/auth/logout/`
Cierra sesión.

**Headers:**
```
X-Session-Token: <token>  (opcional, usa cookie)
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout exitoso",
  "timestamp": "2026-02-06T02:00:00Z"
}
```

#### `GET /api/v1/auth/verify/`
Verifica sesión actual.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Sesión válida",
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      ...
    }
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

#### `GET /api/v1/auth/me/`
Obtiene usuario actual.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin User",
      "role": "administrador",
      "is_active": true,
      "last_login": "2026-02-06T01:00:00Z"
    }
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

### Usuarios

#### `GET /api/v1/users/`
Lista usuarios con paginación.

**Query Params:**
- `page` (int, default: 1)
- `page_size` (int, default: 20, max: 100)
- `search` (str, optional)
- `role` (str, optional: 'administrador', 'usuario')
- `is_active` (bool, optional)

**Response (200 OK):**
```json
{
  "success": true,
  "items": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

#### `POST /api/v1/users/create/`
Crea nuevo usuario (solo administradores).

**Request:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "full_name": "New User",
  "role": "usuario"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "user": {
      "id": 2,
      "username": "newuser",
      "email": "newuser@example.com",
      "full_name": "New User",
      "role": "usuario",
      "is_active": true
    }
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

#### `GET /api/v1/users/{id}/`
Obtiene detalles de usuario.

#### `PUT/PATCH /api/v1/users/{id}/update/`
Actualiza usuario (solo administradores).

#### `DELETE /api/v1/users/{id}/delete/`
Elimina usuario (solo administradores).

### Sistema

#### `GET /api/v1/health/`
Verificación de salud.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "service": "WebAMG API v1"
  },
  "timestamp": "2026-02-06T02:00:00Z"
}
```

#### `GET /api/v1/info/`
Información de API y endpoints disponibles.

## 🛡️ Mejoras de Seguridad Implementadas

### 1. Autenticación y Autorización
- ✅ Token de sesión seguro (64 caracteres URL-safe)
- ✅ Expiración de sesión (8 horas)
- ✅ Validación de roles por endpoint
- ✅ Prevención de CSRF con cookies HttpOnly
- ✅ SameSite=Lax para cookies

### 2. Protección Contra Ataques
- ✅ Rate limiting para prevenir fuerza bruta
- ✅ Sanitización de input (XSS, SQL Injection)
- ✅ Validación de datos con Pydantic
- ✅ Headers de seguridad HTTP
- ✅ Content Security Policy

### 3. Logging y Auditoría
- ✅ Logging de todas las requests
- ✅ Registro de intentos fallidos de login
- ✅ Logs separados por seguridad
- ✅ Registro de IP y User-Agent

### 4. Manejo de Errores
- ✅ Respuestas de error estructuradas
- ✅ Códigos de error específicos
- ✅ Detalles de error opcionales (DEBUG mode)
- ✅ No exposición de información sensible

### 5. Validación de Datos
- ✅ Validación de emails
- ✅ Validación de passwords (mayúsculas, minúsculas, números)
- ✅ Validación de usernames (3-30 caracteres, alfanumérico)
- ✅ Validación de números de teléfono (formato Guatemala)
- ✅ Validación de fechas

## 📝 Checklist de Seguridad para Nuevos Endpoints

Antes de crear un nuevo endpoint de API, asegúrate de:

1. ✅ Usar el decorador `@api_endpoint` con las opciones apropiadas
2. ✅ Validar inputs con modelos Pydantic
3. ✅ Sanitizar datos de usuario
4. ✅ Aplicar rate limiting si es necesario
5. ✅ Implementar autorización basada en roles
6. ✅ Agregar logging apropiado
7. ✅ Manejar excepciones con tipos específicos
8. ✅ Usar `APIResponse` para respuestas consistentes
9. ✅ Documentar el endpoint (Swagger/OpenAPI si es posible)
10. ✅ Probar casos de error y seguridad

## 🧪 Testing

### Ejemplos de Pruebas con cURL

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"SecurePass123"}'
```

#### Obtener usuario actual
```bash
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Cookie: session_token=<token>"
```

#### Crear usuario (requiere admin)
```bash
curl -X POST http://localhost:8000/api/v1/users/create/ \
  -H "Content-Type: application/json" \
  -H "Cookie: session_token=<admin_token>" \
  -d '{
    "username":"newuser",
    "email":"newuser@example.com",
    "password":"SecurePass123",
    "full_name":"New User"
  }'
```

## 📚 Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [REST API Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Django Security Documentation](https://docs.djangoproject.com/en/6.0/topics/security/)

## ⚠️ Notas Importantes

1. **Contraseñas**: En producción, considera migrar de SHA-256 a bcrypt o Argon2
2. **HTTPS**: Siempre usa HTTPS en producción para proteger tokens y datos
3. **Rate Limiting**: Ajusta los límites según tus necesidades de uso
4. **Logs**: Implementa rotación de logs para evitar que llenen el disco
5. **Monitoreo**: Configura alertas para errores de seguridad y rate limiting
6. **Dependencias**: Mantén todas las dependencias actualizadas

## 🔄 Plan de Migración desde APIs Antiguas

Las APIs en `/api/...` (sin versión) seguirán funcionando por compatibilidad, pero se recomienda migrar a `/api/v1/...`:

1. Reemplazar URLs de endpoint
2. Actualizar manejo de respuestas (formato `APIResponse`)
3. Agregar headers de autenticación apropiados
4. Actualizar manejo de errores

## 📞 Soporte

Para preguntas o reportes de seguridad, contacta al equipo de desarrollo.
