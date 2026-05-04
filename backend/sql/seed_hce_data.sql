-- =============================================================================
-- SCRIPT: Insertar datos de prueba en HCE (Historia Clínica Electrónica)
-- =============================================================================
-- Este script inserta antecedentes y consultas previas para pacientes existentes
-- Requiere: Pacientes ya creados en la tabla 'pacientes'
-- =============================================================================

-- Insertar antecedentes médicos para pacientes
-- Tipos válidos: Alergia, Patologia, Cirugia, Medicamento

INSERT INTO hce_antecedentes (paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo, version, created_at, updated_at) VALUES
-- Paciente 1 (asumiendo ID 1 existe)
(1, 'Patologia', 'Hipertensión Arterial', 'Diagnosticada hace 5 años, controlada con medicación', '2019-03-15', true, 1, NOW(), NOW()),
(1, 'Medicamento', 'Losartán 50mg', '1 tableta cada 24 horas', NULL, true, 1, NOW(), NOW()),
(1, 'Alergia', 'Penicilina', 'Reacción leve de rash cutáneo', NULL, true, 1, NOW(), NOW()),

-- Paciente 2 (asumiendo ID 2 existe)
(2, 'Patologia', 'Diabetes Mellitus Tipo 2', 'Diagnosticada en 2018, en tratamiento con metformina', '2018-07-20', true, 1, NOW(), NOW()),
(2, 'Medicamento', 'Metformina 850mg', '1 tableta con cada comida', NULL, true, 1, NOW(), NOW()),
(2, 'Cirugia', 'Apendicectomía', 'Cirugía realizada en 2015 sin complicaciones', '2015-11-10', true, 1, NOW(), NOW()),

-- Paciente 3 (asumiendo ID 3 existe)
(3, 'Alergia', 'Ioduro', 'Reacción alérgica a contrastes con yodo', NULL, true, 1, NOW(), NOW()),
(3, 'Patologia', 'Asma', 'Asma leve, controlada con salbutamol inhalado', '2010-05-12', true, 1, NOW(), NOW()),

-- Paciente 4 (asumiendo ID 4 existe)
(4, 'Patologia', 'Dislipidemia', 'Colesterol elevado, en tratamiento con estatinas', '2020-01-15', true, 1, NOW(), NOW()),
(4, 'Medicamento', 'Atorvastatina 20mg', '1 tableta en las noches', NULL, true, 1, NOW(), NOW()),

-- Paciente 5 (asumiendo ID 5 existe)
(5, 'Patologia', 'Gastritis Crónica', 'Reflujo gastroesofágico, tratamiento con omeprazol', '2017-09-03', true, 1, NOW(), NOW()),
(5, 'Cirugia', 'Cesárea', 'Cirugía realizada en 2019', '2019-08-22', true, 1, NOW(), NOW()),
(5, 'Medicamento', 'Omeprazol 20mg', '1 tableta en ayunas', NULL, true, 1, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Insertar consultas previas para pacientes
INSERT INTO hce_consulta_previa (paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento, version, created_at, updated_at) VALUES

-- Paciente 1 - Consultas previas
(1, '2023-12-10 09:30:00', 'Control de presión arterial', 'HTA controlada', 'Continuar Losartán, control en 3 meses', 1, NOW(), NOW()),
(1, '2024-02-15 10:15:00', 'Dolor de cabeza leve', 'Cefalea tensional', 'Paracetamol 500mg cada 8h por 3 días', 1, NOW(), NOW()),
(1, '2024-05-20 08:45:00', 'Control rutinario', 'Paciente estable', 'Mantener tratamiento actual', 1, NOW(), NOW()),

-- Paciente 2 - Consultas previas
(2, '2023-11-05 14:00:00', 'Control diabetes', 'DM2 con HbA1c 7.2%', 'Ajustar metformina, dieta hipoglucida', 1, NOW(), NOW()),
(2, '2024-01-20 11:30:00', 'Infección respiratoria', 'Faringitis aguda', 'Amoxicilina 500mg cada 8h por 7 días', 1, NOW(), NOW()),
(2, '2024-04-12 09:00:00', 'Control diabetes', 'DM2 estable', 'Continuar metformina', 1, NOW(), NOW()),

-- Paciente 3 - Consultas previas
(3, '2023-10-18 16:45:00', 'Exacerbación asmática', 'Asma moderada exacerbada', 'Prednisona 40mg por 5 días + Salbutamol', 1, NOW(), NOW()),
(3, '2024-03-08 10:00:00', 'Control asma', 'Asma bien controlada', 'Continuar tratamiento inhalado', 1, NOW(), NOW()),

-- Paciente 4 - Consultas previas
(4, '2024-01-10 08:30:00', 'Control colesterol', 'Dislipidemia mixta', 'Iniciar Atorvastatina, control en 2 meses', 1, NOW(), NOW()),
(4, '2024-03-25 09:15:00', 'Dolor muscular', 'Mialgia probablemente secundaria a estatina', 'Reducir dosis de atorvastatina', 1, NOW(), NOW()),

-- Paciente 5 - Consultas previas
(5, '2023-12-22 11:00:00', 'Dolor epigástrico', 'Gastritis aguda', 'Omeprazol 20mg por 14 días + dieta blanda', 1, NOW(), NOW()),
(5, '2024-02-28 14:30:00', 'Control prenatal', 'Embarazo de 32 semanas sin complicaciones', 'Continuar control obstétrico', 1, NOW(), NOW()),
(5, '2024-05-05 10:45:00', 'Consulta post-parto', 'Periodo post-parto normal', 'Continuar control', 1, NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Verificar datos insertados
SELECT 'Antecedentes insertados: ' || COUNT(*)::text as resultado FROM hce_antecedentes WHERE created_at > NOW() - interval '1 minute'
UNION ALL
SELECT 'Consultas previas insertadas: ' || COUNT(*)::text FROM hce_consulta_previa WHERE created_at > NOW() - interval '1 minute';
