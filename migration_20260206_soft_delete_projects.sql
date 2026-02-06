-- =====================================================
-- MIGRACIÓN: Soft Delete de Proyectos
-- Fecha: 2026-02-06
-- Descripción: Implementación de soft delete para proyectos
--              usando el campo is_active con propagación en cascada
-- =====================================================

-- Configurar zona horaria
SET TIME ZONE 'America/Guatemala';

-- =====================================================
-- PASO 1: Agregar campo is_active a tablas relacionadas
-- =====================================================

-- Fases de proyectos
ALTER TABLE project_phases ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_phases_is_active ON project_phases(is_active);

-- Relación proyectos-beneficiarios
ALTER TABLE project_beneficiaries ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_project_beneficiaries_is_active ON project_beneficiaries(is_active);

-- Relación fases-beneficiarios
ALTER TABLE phase_beneficiaries ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_phase_beneficiaries_is_active ON phase_beneficiaries(is_active);

-- Materiales de proyectos
ALTER TABLE project_materials ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_materials_is_active ON project_materials(is_active);

-- Actividades diarias
ALTER TABLE daily_activities ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_activities_is_active ON daily_activities(is_active);

-- Fotos de actividades
ALTER TABLE activity_photos ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_activity_photos_is_active ON activity_photos(is_active);

-- Evidencias de proyectos
ALTER TABLE project_evidences ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_evidences_is_active ON project_evidences(is_active);

-- Evidencias de fases
ALTER TABLE phase_evidences ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_phase_evidences_is_active ON phase_evidences(is_active);

-- Fotos de evidencias de proyectos
ALTER TABLE evidence_photos ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_evidence_photos_is_active ON evidence_photos(is_active);

-- Fotos de evidencias de fases
ALTER TABLE phase_evidence_photos ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_phase_evidence_photos_is_active ON phase_evidence_photos(is_active);

-- Relación evidencias-beneficiarios
ALTER TABLE evidence_beneficiaries ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_evidence_beneficiaries_is_active ON evidence_beneficiaries(is_active);

-- Relación evidencias de fases-beneficiarios
ALTER TABLE phase_evidence_beneficiaries ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_phase_evidence_beneficiaries_is_active ON phase_evidence_beneficiaries(is_active);

-- Ejecución presupuestaria
ALTER TABLE budget_execution ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
CREATE INDEX IF NOT EXISTS idx_budget_execution_is_active ON budget_execution(is_active);

-- =====================================================
-- PASO 2: Crear trigger para propagar estado del proyecto
-- =====================================================

CREATE OR REPLACE FUNCTION propagate_project_deactivation()
RETURNS TRIGGER AS $$
BEGIN
    -- Si is_active cambió
    IF OLD.is_active IS DISTINCT FROM NEW.is_active THEN
        -- Actualizar fases
        UPDATE project_phases
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE project_id = NEW.id;

        -- Actualizar relación proyectos-beneficiarios
        UPDATE project_beneficiaries
        SET is_active = NEW.is_active
        WHERE project_id = NEW.id;

        -- Actualizar materiales
        UPDATE project_materials
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE project_id = NEW.id;

        -- Actualizar actividades diarias del proyecto
        UPDATE daily_activities
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE project_id = NEW.id;

        -- Actualizar evidencias del proyecto
        UPDATE project_evidences
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE project_id = NEW.id;

        -- Actualizar ejecución presupuestaria del proyecto
        UPDATE budget_execution
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE project_id = NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger en tabla projects
DROP TRIGGER IF EXISTS trigger_propagate_project_deactivation ON projects;
CREATE TRIGGER trigger_propagate_project_deactivation
    AFTER UPDATE OF is_active ON projects
    FOR EACH ROW
    EXECUTE FUNCTION propagate_project_deactivation();

COMMENT ON FUNCTION propagate_project_deactivation IS 'Propaga el estado is_active de un proyecto a todas sus tablas relacionadas';

-- =====================================================
-- PASO 3: Crear trigger para propagar estado de fases
-- =====================================================

CREATE OR REPLACE FUNCTION propagate_phase_deactivation()
RETURNS TRIGGER AS $$
BEGIN
    -- Si is_active cambió
    IF OLD.is_active IS DISTINCT FROM NEW.is_active THEN
        -- Actualizar relación fases-beneficiarios
        UPDATE phase_beneficiaries
        SET is_active = NEW.is_active
        WHERE phase_id = NEW.id;

        -- Actualizar actividades diarias de la fase
        UPDATE daily_activities
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE phase_id = NEW.id;

        -- Actualizar evidencias de la fase
        UPDATE phase_evidences
        SET is_active = NEW.is_active, updated_at = CURRENT_TIMESTAMP
        WHERE phase_id = NEW.id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger en tabla project_phases
DROP TRIGGER IF EXISTS trigger_propagate_phase_deactivation ON project_phases;
CREATE TRIGGER trigger_propagate_phase_deactivation
    AFTER UPDATE OF is_active ON project_phases
    FOR EACH ROW
    EXECUTE FUNCTION propagate_phase_deactivation();

COMMENT ON FUNCTION propagate_phase_deactivation IS 'Propaga el estado is_active de una fase a todas sus tablas relacionadas';

-- =====================================================
-- PASO 4: Crear trigger para propagar estado de evidencias
-- =====================================================

CREATE OR REPLACE FUNCTION propagate_evidence_deactivation()
RETURNS TRIGGER AS $$
BEGIN
    -- Si is_active cambió
    IF OLD.is_active IS DISTINCT FROM NEW.is_active THEN
        -- Determinar el tipo de evidencia
        IF TG_TABLE_NAME = 'project_evidences' THEN
            -- Actualizar relación evidencias-beneficiarios (proyectos)
            UPDATE evidence_beneficiaries
            SET is_active = NEW.is_active
            WHERE evidence_id = NEW.id;

            -- Actualizar fotos de evidencias de proyectos
            UPDATE evidence_photos
            SET is_active = NEW.is_active
            WHERE evidence_id = NEW.id;

        ELSIF TG_TABLE_NAME = 'phase_evidences' THEN
            -- Actualizar relación evidencias-beneficiarios (fases)
            UPDATE phase_evidence_beneficiaries
            SET is_active = NEW.is_active
            WHERE phase_evidence_id = NEW.id;

            -- Actualizar fotos de evidencias de fases
            UPDATE phase_evidence_photos
            SET is_active = NEW.is_active
            WHERE phase_evidence_id = NEW.id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger en tabla project_evidences
DROP TRIGGER IF EXISTS trigger_propagate_project_evidence_deactivation ON project_evidences;
CREATE TRIGGER trigger_propagate_project_evidence_deactivation
    AFTER UPDATE OF is_active ON project_evidences
    FOR EACH ROW
    EXECUTE FUNCTION propagate_evidence_deactivation();

-- Crear trigger en tabla phase_evidences
DROP TRIGGER IF EXISTS trigger_propagate_phase_evidence_deactivation ON phase_evidences;
CREATE TRIGGER trigger_propagate_phase_evidence_deactivation
    AFTER UPDATE OF is_active ON phase_evidences
    FOR EACH ROW
    EXECUTE FUNCTION propagate_evidence_deactivation();

COMMENT ON FUNCTION propagate_evidence_deactivation IS 'Propaga el estado is_active de una evidencia a sus fotos y relaciones con beneficiarios';

-- =====================================================
-- PASO 5: Actualizar vistas para filtrar por is_active
-- =====================================================

-- Actualizar vista de resumen de proyectos
DROP VIEW IF EXISTS v_projects_summary CASCADE;
CREATE VIEW v_projects_summary AS
SELECT
    p.id,
    p.project_name,
    p.project_code,
    p.status,
    p.start_date,
    p.end_date,
    p.progress_percentage,
    p.municipality,
    p.department,
    p.estimated_budget,
    p.actual_budget,
    u.full_name AS responsible_name,
    COUNT(DISTINCT pb.beneficiary_id) AS total_beneficiaries,
    COUNT(DISTINCT pp.id) AS total_phases,
    COALESCE(SUM(pm.total_cost), 0) AS total_materials_cost,
    COUNT(DISTINCT be.id) AS total_invoices,
    COALESCE(SUM(be.total_amount), 0) AS total_executed
FROM projects p
LEFT JOIN users u ON p.responsible_user = u.id
LEFT JOIN project_beneficiaries pb ON p.id = pb.project_id AND pb.is_active = TRUE
LEFT JOIN project_phases pp ON p.id = pp.project_id AND pp.is_active = TRUE
LEFT JOIN project_materials pm ON p.id = pm.project_id AND pm.is_active = TRUE
LEFT JOIN budget_execution be ON p.id = be.project_id AND be.is_active = TRUE AND be.is_approved = TRUE
WHERE p.is_active = TRUE
GROUP BY p.id, u.full_name;

-- Actualizar vista de ejecución presupuestaria por proyecto
DROP VIEW IF EXISTS v_budget_execution_by_project CASCADE;
CREATE VIEW v_budget_execution_by_project AS
SELECT
    p.id AS project_id,
    p.project_name,
    p.project_code,
    p.estimated_budget,
    p.actual_budget,
    COUNT(be.id) AS total_invoices,
    COALESCE(SUM(be.total_amount), 0) AS total_executed,
    COALESCE(SUM(CASE WHEN be.is_paid THEN be.total_amount ELSE 0 END), 0) AS total_paid,
    COALESCE(SUM(CASE WHEN NOT be.is_paid THEN be.total_amount ELSE 0 END), 0) AS total_pending,
    CASE
        WHEN p.estimated_budget > 0 THEN
            ROUND((COALESCE(SUM(be.total_amount), 0) / p.estimated_budget * 100), 2)
        ELSE 0
    END AS execution_percentage,
    CASE
        WHEN p.estimated_budget > 0 THEN
            p.estimated_budget - COALESCE(SUM(be.total_amount), 0)
        ELSE 0
    END AS budget_remaining
FROM projects p
LEFT JOIN budget_execution be ON p.id = be.project_id AND be.is_active = TRUE AND be.is_approved = TRUE
WHERE p.is_active = TRUE
GROUP BY p.id, p.project_name, p.project_code, p.estimated_budget, p.actual_budget;

-- Actualizar vista de ejecución presupuestaria por fase
DROP VIEW IF EXISTS v_budget_execution_by_phase CASCADE;
CREATE VIEW v_budget_execution_by_phase AS
SELECT
    pp.id AS phase_id,
    pp.phase_name,
    pp.project_id,
    p.project_name,
    pp.estimated_budget,
    pp.actual_budget,
    COUNT(be.id) AS total_invoices,
    COALESCE(SUM(be.total_amount), 0) AS total_executed,
    COALESCE(SUM(CASE WHEN be.is_paid THEN be.total_amount ELSE 0 END), 0) AS total_paid,
    COALESCE(SUM(CASE WHEN NOT be.is_paid THEN be.total_amount ELSE 0 END), 0) AS total_pending,
    CASE
        WHEN pp.estimated_budget > 0 THEN
            ROUND((COALESCE(SUM(be.total_amount), 0) / pp.estimated_budget * 100), 2)
        ELSE 0
    END AS execution_percentage
FROM project_phases pp
JOIN projects p ON pp.project_id = p.id AND p.is_active = TRUE AND pp.is_active = TRUE
LEFT JOIN budget_execution be ON pp.id = be.phase_id AND be.is_active = TRUE AND be.is_approved = TRUE
WHERE p.is_active = TRUE AND pp.is_active = TRUE
GROUP BY pp.id, pp.phase_name, pp.project_id, p.project_name, pp.estimated_budget, pp.actual_budget;

-- Actualizar vista de actividades recientes
DROP VIEW IF EXISTS v_recent_activities CASCADE;
CREATE VIEW v_recent_activities AS
SELECT
    da.id,
    da.activity_date,
    da.activity_type,
    da.description,
    COALESCE(p.project_name, 'Fase: ' || pp.phase_name) AS project_or_phase,
    u.full_name AS created_by_name,
    COUNT(ap.id) AS photos_count
FROM daily_activities da
LEFT JOIN projects p ON da.project_id = p.id AND p.is_active = TRUE
LEFT JOIN project_phases pp ON da.phase_id = pp.id AND pp.is_active = TRUE
LEFT JOIN users u ON da.created_by = u.id
LEFT JOIN activity_photos ap ON da.id = ap.activity_id AND ap.is_active = TRUE
WHERE da.is_active = TRUE
GROUP BY da.id, p.project_name, pp.phase_name, u.full_name
ORDER BY da.activity_date DESC;

-- =====================================================
-- PASO 6: Verificar migración
-- =====================================================

-- Verificar que todos los campos is_active se agregaron correctamente
SELECT
    'project_phases' AS tabla, COUNT(*) AS total, SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS activos
FROM project_phases
UNION ALL
SELECT
    'project_beneficiaries', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM project_beneficiaries
UNION ALL
SELECT
    'project_materials', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM project_materials
UNION ALL
SELECT
    'daily_activities', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM daily_activities
UNION ALL
SELECT
    'project_evidences', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM project_evidences
UNION ALL
SELECT
    'phase_evidences', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM phase_evidences
UNION ALL
SELECT
    'budget_execution', COUNT(*), SUM(CASE WHEN is_active THEN 1 ELSE 0 END)
FROM budget_execution
ORDER BY tabla;

-- =====================================================
-- FIN DE LA MIGRACIÓN
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Migración completada exitosamente!';
    RAISE NOTICE '========================================';
    RAISE NOTICE '';
    RAISE NOTICE 'Campos is_active agregados a:';
    RAISE NOTICE '  - project_phases';
    RAISE NOTICE '  - project_beneficiaries';
    RAISE NOTICE '  - phase_beneficiaries';
    RAISE NOTICE '  - project_materials';
    RAISE NOTICE '  - daily_activities';
    RAISE NOTICE '  - activity_photos';
    RAISE NOTICE '  - project_evidences';
    RAISE NOTICE '  - phase_evidences';
    RAISE NOTICE '  - evidence_photos';
    RAISE NOTICE '  - phase_evidence_photos';
    RAISE NOTICE '  - evidence_beneficiaries';
    RAISE NOTICE '  - phase_evidence_beneficiaries';
    RAISE NOTICE '  - budget_execution';
    RAISE NOTICE '';
    RAISE NOTICE 'Triggers creados:';
    RAISE NOTICE '  - propagate_project_deactivation';
    RAISE NOTICE '  - propagate_phase_deactivation';
    RAISE NOTICE '  - propagate_evidence_deactivation';
    RAISE NOTICE '';
    RAISE NOTICE 'Vistas actualizadas para filtrar is_active';
    RAISE NOTICE '========================================';
END $$;
