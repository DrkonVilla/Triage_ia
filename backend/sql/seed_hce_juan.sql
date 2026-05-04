-- =============================================================================
-- SCRIPT: Insertar HCE para Juan Martínez García (DNI: 87654321B)
-- =============================================================================

-- Insertar antecedentes médicos para Juan (ID 6 basado en logs anteriores)
INSERT INTO hce_antecedentes (paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo, version, created_at, updated_at)
SELECT 
    p.id,
    unnest(ARRAY['Patologia', 'Medicamento', 'Cirugia', 'Alergia']) as tipo,
    unnest(ARRAY[
        'Diabetes Mellitus Tipo 2',
        'Metformina 850mg',
        'Bypass gástrico (2019)',
        'Sulfonamidas'
    ]) as nombre,
    unnest(ARRAY[
        'Diagnosticada en 2018, controlada con dieta y medicación',
        'Tomar 1 tableta con el desayuno y la cena',
        'Cirugía bariátrica realizada en Clínica Mayo, evolución favorable',
        'Reacción severa - evitar todo tipo de sulfonamidas'
    ]) as descripcion,
    unnest(ARRAY[
        '2018-03-15'::date,
        NULL::date,
        '2019-07-20'::date,
        NULL::date
    ]) as fecha_diagnostico,
    true,
    1,
    NOW(),
    NOW()
FROM pacientes p
WHERE p.dni = '87654321B'  -- Juan Martínez García
ON CONFLICT DO NOTHING;

-- Insertar consultas previas para Juan
INSERT INTO hce_consulta_previa (paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento, version, created_at, updated_at)
SELECT 
    p.id,
    fecha_consulta,
    motivo,
    diagnostico,
    tratamiento,
    1,
    NOW(),
    NOW()
FROM pacientes p
CROSS JOIN (
    VALUES 
        ('2023-08-15 09:30:00'::timestamp, 'Control diabetes', 'DM2 - HbA1c 7.8%', 'Ajustar dosis metformina, control en 3 meses'),
        ('2023-11-20 10:15:00', 'Control rutinario', 'Paciente estable, peso 85kg', 'Continuar tratamiento actual'),
        ('2024-02-10 08:45:00', 'Dolor abdominal', 'Gastritis leve', 'Omeprazol 20mg por 14 días'),
        ('2024-05-05 11:00:00', 'Control diabetes', 'DM2 - HbA1c 7.2%, mejoría', 'Mantener tratamiento'),
        ('2024-09-12 14:30:00', 'Hipertensión arterial detectada', 'HTA grado 1', 'Iniciar Losartán 50mg, control en 1 mes')
) AS t(fecha_consulta, motivo, diagnostico, tratamiento)
WHERE p.dni = '87654321B'
ON CONFLICT DO NOTHING;

-- Verificar inserción
SELECT 'Antecedentes de Juan: ' || COUNT(*)::text as resultado 
FROM hce_antecedentes a 
JOIN pacientes p ON a.paciente_id = p.id 
WHERE p.dni = '87654321B'
UNION ALL
SELECT 'Consultas previas de Juan: ' || COUNT(*)::text 
FROM hce_consulta_previa c 
JOIN pacientes p ON c.paciente_id = p.id 
WHERE p.dni = '87654321B';
