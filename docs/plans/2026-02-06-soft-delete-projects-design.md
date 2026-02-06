# Soft Delete de Proyectos - Diseño Técnico

**Fecha:** 2026-02-06  
**Autor:** OpenCode  
**Versión:** 1.0

## Resumen

Implementación de soft delete para proyectos, permitiendo desactivarlos en lugar de eliminarlos completamente. Los proyectos desactivados pueden reactivarse en el futuro. La solución utiliza triggers en cascada para propagar el estado `is_active = FALSE` a todas las tablas relacionadas (fases, beneficiarios, evidencias, materiales, actividades, presupuesto ejecutado, etc.).

## Objetivos

- Mantener integridad de datos históricos
- Permitir reactivación de proyectos cuando sea necesario
- Ocultar automáticamente todos los datos relacionados cuando se desactiva un proyecto
- Implementar con mínimo impacto en código existente

## Arquitectura General

El diseño utiliza el patrón **soft delete** con el campo `is_active` que ya existe en la tabla `projects`. Cuando un usuario "elimina" un proyecto, en realidad solo se marca como inactivo, lo que permite reactivarlo en el futuro.

La implementación utiliza **triggers en cascada** que automáticamente propagan el estado `is_active = FALSE` a todas las tablas relacionadas.

### Flujo de Operación

1. La aplicación Django actualiza `projects.is_active = FALSE`
2. Un trigger detecta el cambio y marca como inactivas todas las filas relacionadas
3. Un trigger secundario detecta cambios en `project_phases` y marca como inactivas las `phase_evidences` relacionadas
4. Todas las consultas de la aplicación filtran automáticamente por `is_active = TRUE`

### Ventajas

- Los datos nunca se pierden
- Las consultas son simples (solo WHERE is_active)
- La reactivación es igual de sencilla (UPDATE is_active = TRUE propagado por los mismos triggers)

## Estructura de la Base de Datos

### Nuevos Campos

Las siguientes tablas necesitan agregar el campo `is_active`:

| Tabla | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `project_phases` | BOOLEAN | TRUE | Estado de activo de la fase |
| `project_beneficiaries` | BOOLEAN | TRUE | Estado de la relación proyecto-beneficiario |
| `project_materials` | BOOLEAN | TRUE | Estado del material del proyecto |
| `project_evidences` | BOOLEAN | TRUE | Estado de la evidencia del proyecto |
| `phase_evidences` | BOOLEAN | TRUE | Estado de la evidencia de la fase |
| `daily_activities` | BOOLEAN | TRUE | Estado de la actividad diaria |
| `budget_execution` | BOOLEAN | TRUE | Estado de la factura/gasto |
| `evidence_beneficiaries` | BOOLEAN | TRUE | Estado de la relación evidencia-beneficiario |
| `phase_evidence_beneficiaries` | BOOLEAN | TRUE | Estado de la relación fase-evidencia-beneficiario |

### Índices

Cada tabla con campo `is_active` debe tener un índice:

```sql
CREATE INDEX idx_{tabla}_is_active ON {tabla}(is_active);
```

### Triggers

**Trigger 1: `propagate_project_deactivation`**

Detecta cambios en `projects.is_active` y propaga a:
- `project_phases`
- `project_beneficiaries`
- `project_materials`
- `project_evidences`
- `daily_activities`
- `budget_execution`

**Trigger 2: `propagate_phase_deactivation`**

Detecta cambios en `project_phases.is_active` y propaga a:
- `phase_evidences`
- `phase_beneficiaries`
- `daily_activities` (asociadas a la fase)

**Trigger 3: `propagate_evidence_deactivation`**

Detecta cambios en `project_evidences.is_active` y `phase_evidences.is_active` y propaga a:
- `evidence_beneficiaries` / `phase_evidence_beneficiaries`
- `evidence_photos` / `phase_evidence_photos`

## Flujo de Datos

### Escenario 1: Desactivar un Proyecto

1. Usuario hace clic en "Eliminar proyecto" en la interfaz
2. Django API endpoint `/api/v1/projects/{id}/deactivate` recibe la solicitud
3. Se verifica que el usuario tenga rol `administrador`
4. Se ejecuta: `UPDATE projects SET is_active = FALSE WHERE id = {id}`
5. **Trigger 1** se dispara y desactiva todas las tablas hijas directas
6. **Trigger 2** se dispara por cada fase desactivada y desactiva sus evidencias
7. **Trigger 3** se dispara por cada evidencia desactivada y desactiva sus relaciones
8. Se retorna respuesta: `{'success': True, 'message': 'Proyecto desactivado'}`

### Escenario 2: Reactivar un Proyecto

Mismo flujo pero con `UPDATE projects SET is_active = TRUE WHERE id = {id}`, propagando en cascada a TRUE.

### Escenario 3: Consultar Proyectos

Todas las consultas Django incluyen `WHERE is_active = TRUE` o `WHERE is_active = FALSE` según el caso.

## Manejo de Errores y Validaciones

### Validaciones en Django

1. **Solo administradores pueden desactivar/reactivar**
   - Decorador `@api_require_roles({'administrador'})`
   - Retorna 401 si usuario no tiene permisos

2. **Proyecto ya en ese estado**
   - Desactivar ya inactivo → 400 `{'error': 'El proyecto ya está inactivo'}`
   - Reactivar ya activo → 400 `{'error': 'El proyecto ya está activo'}`

3. **Proyecto no existe**
   - Retorna 404 `{'error': 'Proyecto no encontrado'}`

### Validaciones en PostgreSQL

1. **Constraint para evitar referencias rotas**
   - Verificar que al reactivar no rompa constraints
   - Si ocurre, el trigger lanza excepción que Django captura

### Validaciones en Frontend

1. **Confirmación de eliminación**
   - Modal: "¿Estás seguro de desactivar este proyecto? Toda su información quedará oculta pero podrás reactivarlo después."

2. **Estado visual del proyecto**
   - Proyectos inactivos: estilo diferente (gris/atenuado)
   - Botón "Desactivar" se cambia por "Reactivar"

### Manejo de Errores en API

- Try/except en todos los endpoints de desactivación/reactivación
- Registro de errores en logs
- Mensajes claros al usuario en español

## Pruebas

### Pruebas Unitarias Django

1. `test_deactivate_project()`
   - Verifica is_active = FALSE
   - Verifica cascada a todas las tablas relacionadas

2. `test_reactivate_project()`
   - Verifica is_active = TRUE
   - Verifica reactivación en cascada

3. `test_deactivate_only_admin()`
   - Usuario normal → 401
   - Administrador → 200

4. `test_query_only_active_projects()`
   - Proyectos activos visibles
   - Proyectos inactivos solo en listas de "archivados"

### Pruebas de Integración PostgreSQL

1. `test_trigger_propagation()` - Ejecuta UPDATE directo y verifica cascada
2. `test_performance_with_is_active_index()` - Verifica rendimiento con índices

## Documentación Necesaria

### Actualizar AGENTS.md

- Comandos para desactivar/reactivar proyectos
- Nota sobre soft delete vs hard delete
- Documentación de nuevos campos `is_active`

### Actualizar API_SECURITY.md

- Nuevos endpoints `/api/v1/projects/{id}/deactivate`
- Requerimiento de rol administrador

### Crear Script de Migración

Archivo: `migration_20260206_soft_delete_projects.sql`

## Componentes Django a Modificar

### API Endpoints (webAMG/api/v1.py)

```python
@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def deactivate_project(request, project_id):
    # Marcar proyecto como inactivo
    pass

@api_endpoint(methods=['POST'], auth_required=True, roles={'administrador'})
def activate_project(request, project_id):
    # Reactivar proyecto
    pass
```

### Django Models (webAMG/models.py)

- Agregar campo `is_active` a todos los modelos relacionados
- Actualizar queries para filtrar por `is_active = TRUE` por defecto

### Views (webAMG/views.py y views_pages.py)

- Actualizar listados para incluir filtros de activo/inactivo
- Agregar acción de desactivar/reactivar en interfaces

## Script SQL de Migración

Ver archivo: `migration_20260206_soft_delete_projects.sql`

## Consideraciones de Performance

- Índices en `is_active` para cada tabla modificada
- Considerar particionamiento por `is_active` si la tabla crece mucho (opcional)
- Monitorear tiempo de ejecución de triggers en cascada

## Cronograma de Implementación

1. **Fase 1:** Aplicar script SQL de migración
2. **Fase 2:** Actualizar modelos Django
3. **Fase 3:** Implementar endpoints API
4. **Fase 4:** Actualizar frontend
5. **Fase 5:** Escribir pruebas
6. **Fase 6:** Documentación

## Riesgos y Mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Triggers lentos con muchos datos | Optimizar con índices, probar con carga real |
| Olvidar filtrar `is_active` en alguna query | Revisión de código, pruebas exhaustivas |
| Reactivar proyecto con datos inconsistentes | Validaciones en triggers y Django |
| Confusión entre soft delete y hard delete | Documentación clara, nombres descriptivos |

## Referencias

- `BasedeDatos.txt` - Esquema de base de datos
- `ProcedimientosAlmacenados-DB.txt` - Stored procedures existentes
- `AGENTS.md` - Guía de desarrollo del proyecto
