-- =============================================
-- FIX: Agregar columnas de auditoría faltantes
-- Tablas afectadas: signos_vitales, sintomas_triaje, resultados_ia
-- =============================================

-- 1. signos_vitales
ALTER TABLE signos_vitales 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

UPDATE signos_vitales 
SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP), 
    activo = TRUE, 
    version = 1 
WHERE updated_at IS NULL;

-- 2. sintomas_triaje
ALTER TABLE sintomas_triaje 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

UPDATE sintomas_triaje 
SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP), 
    activo = TRUE, 
    version = 1 
WHERE updated_at IS NULL;

-- 3. resultados_ia
ALTER TABLE resultados_ia 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

UPDATE resultados_ia 
SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP), 
    activo = TRUE, 
    version = 1 
WHERE updated_at IS NULL;

-- 4. hce_antecedentes (si aplica)
ALTER TABLE hce_antecedentes 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

UPDATE hce_antecedentes 
SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP), 
    version = 1 
WHERE updated_at IS NULL;

-- 5. hce_consulta_previa (si aplica)
ALTER TABLE hce_consulta_previa 
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

UPDATE hce_consulta_previa 
SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP), 
    version = 1 
WHERE updated_at IS NULL;

-- Verificación final
SELECT 
    table_name,
    string_agg(column_name, ', ' ORDER BY column_name) as columnas_auditoria
FROM information_schema.columns 
WHERE table_name IN ('signos_vitales', 'sintomas_triaje', 'resultados_ia', 'hce_antecedentes', 'hce_consulta_previa')
AND column_name IN ('updated_at', 'activo', 'version')
GROUP BY table_name
ORDER BY table_name;
