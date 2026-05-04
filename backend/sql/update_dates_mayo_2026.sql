-- Actualizar algunos triajes a mayo 2026 para que aparezcan en el reporte mensual actual
UPDATE triajes SET 
    fecha_hora = '2026-05-01 10:30:00',
    created_at = '2026-05-01 10:30:00'
WHERE id IN (1, 2, 3, 11, 13, 18);

UPDATE triajes SET 
    fecha_hora = '2026-05-02 14:15:00',
    created_at = '2026-05-02 14:15:00'
WHERE id IN (22, 28, 34, 40, 8, 25);

-- Asegurar que haya discrepancias (IA != Humano)
UPDATE triajes SET 
    nivel_urgencia_asignado_ia = 'RED',
    nivel_urgencia_final = 'YELLOW'
WHERE id = 3;  -- Sub-clasificacion

UPDATE triajes SET 
    nivel_urgencia_asignado_ia = 'YELLOW',
    nivel_urgencia_final = 'RED'
WHERE id = 14;  -- Sobre-clasificacion

UPDATE triajes SET 
    nivel_urgencia_asignado_ia = 'GREEN',
    nivel_urgencia_final = 'YELLOW'
WHERE id = 6;  -- Sobre-clasificacion

UPDATE triajes SET 
    nivel_urgencia_asignado_ia = 'ORANGE',
    nivel_urgencia_final = 'YELLOW'
WHERE id = 15;  -- Sub-clasificacion

UPDATE triajes SET 
    nivel_urgencia_asignado_ia = 'BLUE',
    nivel_urgencia_final = 'GREEN'
WHERE id IN (9, 17, 32, 36, 39);  -- Sobre-clasificacion leve

-- Verificar discrepancias en mayo 2026
SELECT id, paciente_id, nivel_urgencia_asignado_ia, nivel_urgencia_final, 
       CASE 
         WHEN nivel_urgencia_asignado_ia != nivel_urgencia_final THEN 'DISCREPANCIA'
         ELSE 'OK'
       END as estado
FROM triajes 
WHERE created_at >= '2026-05-01' AND created_at <= '2026-05-31';
