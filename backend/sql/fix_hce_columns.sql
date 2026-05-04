-- =============================================================================
-- FIX: Agregar columnas faltantes a hce_consulta_previa
-- =============================================================================

-- Agregar columnas de auditoría que faltan en hce_consulta_previa
ALTER TABLE hce_consulta_previa 
    ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT true,
    ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Actualizar registros existentes
UPDATE hce_consulta_previa 
SET activo = true, 
    version = 1, 
    created_at = NOW(), 
    updated_at = NOW()
WHERE activo IS NULL;

-- Verificar que las columnas existen
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'hce_consulta_previa'
ORDER BY ordinal_position;
