-- =============================================
-- Sistema de Triaje Clínico Asistido por IA
-- Base de Datos PostgreSQL 16+
-- =============================================

-- Habilitar extensión para UUID (opcional)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- TABLA: usuarios (Control de acceso)
-- =============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('enfermera', 'medico', 'gerente', 'auditor')),
    activo BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1
);

-- =============================================
-- TABLA: pacientes
-- =============================================
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    dni VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(10) CHECK (genero IN ('M', 'F', 'Otros')),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    CONSTRAINT chk_fecha_nacimiento CHECK (fecha_nacimiento <= CURRENT_DATE)
);

-- =============================================
-- TABLA: contactos_emergencia
-- =============================================
CREATE TABLE IF NOT EXISTS contactos_emergencia (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    nombres_completos VARCHAR(150) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    parentesco VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_contacto_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- =============================================
-- TABLA: triajes
-- =============================================
CREATE TABLE IF NOT EXISTS triajes (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo_consulta TEXT NOT NULL,
    nivel_urgencia_asignado_ia VARCHAR(10) CHECK (nivel_urgencia_asignado_ia IN ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE')),
    nivel_urgencia_final VARCHAR(10) CHECK (nivel_urgencia_final IN ('RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE')),
    estado_logistico VARCHAR(20) DEFAULT 'En Espera' CHECK (estado_logistico IN ('En Espera', 'Llamado', 'En Atencion', 'Atendido')),
    notas_medicas TEXT,
    diagnostico_final_medico TEXT,
    tiempo_atencion_segundos INTEGER,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    CONSTRAINT fk_triaje_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    CONSTRAINT fk_triaje_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- =============================================
-- TABLA: signos_vitales
-- =============================================
CREATE TABLE IF NOT EXISTS signos_vitales (
    id SERIAL PRIMARY KEY,
    triaje_id INTEGER UNIQUE NOT NULL REFERENCES triajes(id) ON DELETE CASCADE,
    presion_sistolica INTEGER CHECK (presion_sistolica BETWEEN 50 AND 250),
    presion_diastolica INTEGER CHECK (presion_diastolica BETWEEN 30 AND 200),
    frecuencia_cardiaca INTEGER CHECK (frecuencia_cardiaca BETWEEN 30 AND 250),
    frecuencia_respiratoria INTEGER CHECK (frecuencia_respiratoria BETWEEN 5 AND 60),
    temperatura DECIMAL(4,1) CHECK (temperatura BETWEEN 30 AND 45),
    saturacion_o2 INTEGER CHECK (saturacion_o2 BETWEEN 0 AND 100),
    nota_suplementaria TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_signos_triaje FOREIGN KEY (triaje_id) REFERENCES triajes(id)
);

-- =============================================
-- TABLA: sintomas_triaje
-- =============================================
CREATE TABLE IF NOT EXISTS sintomas_triaje (
    id SERIAL PRIMARY KEY,
    triaje_id INTEGER NOT NULL REFERENCES triajes(id) ON DELETE CASCADE,
    sintoma VARCHAR(100) NOT NULL,
    intensidad VARCHAR(20) CHECK (intensidad IN ('Leve', 'Moderado', 'Grave')),
    descripcion_libre TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sintomas_triaje FOREIGN KEY (triaje_id) REFERENCES triajes(id)
);

-- =============================================
-- TABLA: resultados_ia
-- =============================================
CREATE TABLE IF NOT EXISTS resultados_ia (
    id SERIAL PRIMARY KEY,
    triaje_id INTEGER UNIQUE NOT NULL REFERENCES triajes(id) ON DELETE CASCADE,
    prompt_enviado TEXT NOT NULL,
    respuesta_raw_llm TEXT NOT NULL,
    diagnosticos_json JSONB,
    recomendaciones_json JSONB,
    modelo_utilizado VARCHAR(50),
    latencia_segundos DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_resultados_ia_triaje FOREIGN KEY (triaje_id) REFERENCES triajes(id)
);

-- =============================================
-- TABLA: hce_antecedentes
-- =============================================
CREATE TABLE IF NOT EXISTS hce_antecedentes (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Alergia', 'Patologia', 'Cirugia', 'Medicamento')),
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_diagnostico DATE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_antecedente_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- =============================================
-- TABLA: hce_consulta_previa
-- =============================================
CREATE TABLE IF NOT EXISTS hce_consulta_previa (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    fecha_consulta TIMESTAMP NOT NULL,
    motivo TEXT,
    diagnostico_medico TEXT,
    tratamiento TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_consulta_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- =============================================
-- TABLA: logs_auditoria (Inmutable)
-- =============================================
CREATE TABLE IF NOT EXISTS logs_auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL,
    accion VARCHAR(20) NOT NULL CHECK (accion IN ('INSERT', 'UPDATE', 'DELETE', 'STATUS_CHANGE')),
    modulo VARCHAR(50) NOT NULL,
    registro_id INTEGER NOT NULL,
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- ÍNDICES ESTRATÉGICOS
-- =============================================

-- Para el tablero de cola médica (Kanban)
CREATE INDEX IF NOT EXISTS idx_triajes_estado_logistico ON triajes(estado_logistico) WHERE activo = true;
CREATE INDEX IF NOT EXISTS idx_triajes_nivel_urgencia_final ON triajes(nivel_urgencia_final);
CREATE INDEX IF NOT EXISTS idx_triajes_fecha_hora ON triajes(fecha_hora DESC);

-- Para búsqueda de pacientes
CREATE INDEX IF NOT EXISTS idx_pacientes_dni ON pacientes(dni) WHERE activo = true;
CREATE INDEX IF NOT EXISTS idx_pacientes_nombres ON pacientes(nombres, apellidos);

-- Para auditoría y reportes
CREATE INDEX IF NOT EXISTS idx_logs_auditoria_timestamp ON logs_auditoria(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_logs_auditoria_modulo ON logs_auditoria(modulo, registro_id);

-- Para dashboards (agregaciones)
CREATE INDEX IF NOT EXISTS idx_triajes_fecha_nivel ON triajes(fecha_hora, nivel_urgencia_final);
CREATE INDEX IF NOT EXISTS idx_sintomas_triaje_sintoma ON sintomas_triaje(sintoma);

-- =============================================
-- FUNCIÓN: Actualizar updated_at automáticamente
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pacientes_updated_at BEFORE UPDATE ON pacientes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_triajes_updated_at BEFORE UPDATE ON triajes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================
-- DATOS SEMILLA (Seed Data)
-- =============================================

-- 1. Roles y Usuarios (contraseña: 'password123' hasheada con bcrypt)
-- Hash generado para demostración (bcrypt rounds=12)
INSERT INTO usuarios (username, email, hashed_password, nombres, apellidos, rol) VALUES
('enfermera1', 'enfermera@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyYw3vZzL4RZNy', 'Ana', 'González', 'enfermera'),
('medico1', 'medico@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyYw3vZzL4RZNy', 'Carlos', 'Ramírez', 'medico'),
('gerente1', 'gerente@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyYw3vZzL4RZNy', 'Laura', 'Fernández', 'gerente'),
('auditor1', 'auditor@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyYw3vZzL4RZNy', 'Roberto', 'Silva', 'auditor')
ON CONFLICT (username) DO NOTHING;

-- 2. Pacientes con antecedentes variados
INSERT INTO pacientes (dni, nombres, apellidos, fecha_nacimiento, genero, telefono, email, activo) VALUES
('12345678A', 'María', 'López Pérez', '1985-03-15', 'F', '600111222', 'maria.lopez@email.com', true),
('87654321B', 'Juan', 'Martínez García', '1972-07-22', 'M', '600333444', 'juan.martinez@email.com', true),
('11223344C', 'Carmen', 'Rodríguez Sánchez', '1990-11-05', 'F', '600555666', 'carmen.rodriguez@email.com', true),
('44332211D', 'José', 'Fernández López', '1965-09-30', 'M', '600777888', 'jose.fernandez@email.com', true),
('99887766E', 'Isabel', 'Gómez Ruiz', '2000-02-28', 'F', '600999000', 'isabel.gomez@email.com', true)
ON CONFLICT (dni) DO NOTHING;

-- 3. Contactos de emergencia
INSERT INTO contactos_emergencia (paciente_id, nombres_completos, telefono, parentesco) VALUES
(1, 'Pedro López', '611222333', 'Hermano'),
(2, 'Ana Martínez', '611444555', 'Esposa'),
(3, 'Luis Rodríguez', '611666777', 'Padre'),
(4, 'Sofía Fernández', '611888999', 'Hija'),
(5, 'Miguel Gómez', '611000111', 'Padre');

-- 4. Antecedentes clínicos (HCE)
INSERT INTO hce_antecedentes (paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo) VALUES
(1, 'Patologia', 'Hipertensión Arterial', 'Paciente en tratamiento con Enalapril 20mg', '2019-06-10', true),
(1, 'Alergia', 'Penicilina', 'Reacción anafiláctica documentada', '2015-03-20', true),
(2, 'Patologia', 'Diabetes Tipo 2', 'Manejo con Metformina 850mg', '2018-11-15', true),
(2, 'Cirugia', 'Colecistectomía', 'Laparoscópica, sin complicaciones', '2020-02-10', true),
(3, 'Patologia', 'Asma Bronquial', 'Control con Salbutamol PRN', '2010-08-05', true),
(4, 'Patologia', 'Insuficiencia Cardíaca', 'Fracción de eyección 35%', '2021-01-20', true),
(5, 'Alergia', 'Camarón', 'Urticaria y angioedema', '2016-09-12', true);

-- 5. Consultas previas (HCE)
INSERT INTO hce_consulta_previa (paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento) VALUES
(1, '2024-01-15 10:30:00', 'Dolor torácico', 'Angina estable', 'Reposo y control de presión'),
(1, '2024-02-20 11:00:00', 'Control hipertensión', 'PA controlada', 'Ajuste de dosis Enalapril'),
(2, '2024-01-10 09:15:00', 'Pie diabético', 'Neuropatía periférica', 'Cuidados locales y control glucémico'),
(3, '2024-01-25 15:45:00', 'Crisis asmática', 'Exacerbación moderada', 'Nebulizaciones con salbutamol'),
(5, '2024-02-01 08:30:00', 'Reacción alérgica', 'Urticaria aguda', 'Antihistamínicos');

-- 6. Triajes de ejemplo en diferentes estados
INSERT INTO triajes (paciente_id, usuario_id, fecha_hora, motivo_consulta, nivel_urgencia_asignado_ia, nivel_urgencia_final, estado_logistico, created_at, version) VALUES
(1, 1, CURRENT_TIMESTAMP - INTERVAL '2 hours', 'Dolor torácico opresivo que irradia a brazo izquierdo', 'RED', 'RED', 'En Espera', CURRENT_TIMESTAMP - INTERVAL '2 hours', 1),
(2, 1, CURRENT_TIMESTAMP - INTERVAL '3 hours', 'Disnea de esfuerzo, saturación 88%', 'RED', 'RED', 'En Atencion', CURRENT_TIMESTAMP - INTERVAL '3 hours', 1),
(3, 1, CURRENT_TIMESTAMP - INTERVAL '4 hours', 'Fiebre 39°C, tos productiva', 'YELLOW', 'YELLOW', 'Llamado', CURRENT_TIMESTAMP - INTERVAL '4 hours', 1),
(4, 1, CURRENT_TIMESTAMP - INTERVAL '5 hours', 'Cefalea intensa, visión borrosa', 'ORANGE', 'ORANGE', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '5 hours', 1),
(5, 1, CURRENT_TIMESTAMP - INTERVAL '6 hours', 'Dolor abdominal epigástrico', 'GREEN', 'GREEN', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '6 hours', 1),
(1, 1, CURRENT_TIMESTAMP - INTERVAL '1 day', 'Mareos y náuseas', 'YELLOW', 'GREEN', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '1 day', 1),
(2, 1, CURRENT_TIMESTAMP - INTERVAL '2 days', 'Dolor lumbar', 'GREEN', 'GREEN', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '2 days', 1),
(3, 1, CURRENT_TIMESTAMP - INTERVAL '3 days', 'Herida cortante en mano', 'YELLOW', 'YELLOW', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '3 days', 1),
(4, 1, CURRENT_TIMESTAMP - INTERVAL '4 days', 'Palpitaciones', 'ORANGE', 'ORANGE', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '4 days', 1),
(5, 1, CURRENT_TIMESTAMP - INTERVAL '5 days', 'Diarrea aguda', 'GREEN', 'GREEN', 'Atendido', CURRENT_TIMESTAMP - INTERVAL '5 days', 1)
ON CONFLICT DO NOTHING;

-- 7. Signos vitales para los triajes
INSERT INTO signos_vitales (triaje_id, presion_sistolica, presion_diastolica, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, saturacion_o2, nota_suplementaria) VALUES
(1, 150, 95, 110, 24, 37.2, 94, 'Dolor 8/10, sudoración'),
(2, 130, 85, 105, 28, 38.5, 88, 'Disnea de pequeños esfuerzos'),
(3, 120, 80, 95, 22, 39.1, 95, 'Tos seca, mal estado general'),
(4, 160, 100, 92, 20, 36.8, 98, 'Visión borrosa, fotofobia'),
(5, 118, 75, 88, 18, 37.0, 99, 'Dolor 5/10, náuseas'),
(6, 125, 82, 90, 16, 36.5, 98, 'Mareos al incorporarse'),
(7, 135, 85, 78, 16, 36.8, 97, 'Dolor lumbar mecánico'),
(8, 110, 70, 110, 20, 37.2, 99, 'Herida superficial en palma'),
(9, 145, 90, 115, 22, 37.1, 96, 'Palpitaciones intermitentes'),
(10, 120, 78, 85, 16, 37.8, 98, 'Diarrea acuosa 3 días');

-- 8. Síntomas asociados
INSERT INTO sintomas_triaje (triaje_id, sintoma, intensidad, descripcion_libre) VALUES
(1, 'Dolor_toracico', 'Grave', 'Opresivo, irradia a brazo izquierdo'),
(1, 'Disnea', 'Moderado', 'Al caminar'),
(2, 'Disnea', 'Grave', 'En reposo'),
(2, 'Cianosis', 'Moderado', 'Lechos ungueales'),
(3, 'Fiebre', 'Moderado', '39°C'),
(3, 'Tos', 'Moderado', 'Productiva'),
(4, 'Cefalea', 'Grave', 'Intensidad 9/10'),
(4, 'Trastorno_visual', 'Moderado', 'Visión borrosa'),
(5, 'Dolor_abdominal', 'Moderado', 'Epigastrio, ardor postprandial'),
(6, 'Mareos', 'Leve', 'Al levantarse'),
(7, 'Dolor_lumbar', 'Moderado', 'Mecánico, mejora con movimiento'),
(8, 'Herida', 'Leve', 'Corte superficial en mano derecha'),
(9, 'Palpitaciones', 'Moderado', 'Inicio súbito, duración 5 minutos');

-- 9. Resultados IA simulados
INSERT INTO resultados_ia (triaje_id, prompt_enviado, respuesta_raw_llm, diagnosticos_json, recomendaciones_json, modelo_utilizado, latencia_segundos) VALUES
(1, 'System: Eres experto en triaje... Paciente con dolor torácico...', '{"nivel_urgencia": "RED", "diagnosticos": ["Síndrome coronario agudo"], "recomendaciones": ["ECG urgente", "Aspirina 300mg"]}', '{"diagnostico_principal": "Síndrome coronario agudo", "diferenciales": ["Embolia pulmonar", "Disección aórtica"]}', '{"conducta_inmediata": "Monitorización continua", "estudios": "Troponina, ECG"}', 'gpt-4-turbo', 2.5),
(2, 'System: Paciente con disnea y saturación 88%...', '{"nivel_urgencia": "RED", "diagnosticos": ["Insuficiencia respiratoria aguda"], "recomendaciones": ["Oxígeno 4L/min", "Gasometría arterial"]}', '{"diagnostico_principal": "Insuficiencia respiratoria hipoxémica", "diferenciales": ["Neumonía grave", "EPOC exacerbado"]}', '{"conducta_inmediata": "Oxigenoterapia", "estudios": "Radiografía de tórax"}', 'gpt-4-turbo', 1.8);

-- 10. Logs de auditoría de ejemplo
INSERT INTO logs_auditoria (usuario_id, accion, modulo, registro_id, datos_anteriores, datos_nuevos, ip_address, user_agent) VALUES
(1, 'INSERT', 'triaje', 1, NULL, '{"paciente_id": 1, "nivel_urgencia_final": "RED"}'::jsonb, '192.168.1.100', 'Streamlit/1.30'),
(1, 'STATUS_CHANGE', 'estado_logistico', 1, '"En Espera"', '"En Atencion"', '192.168.1.101', 'Streamlit/1.30'),
(2, 'UPDATE', 'triaje', 3, '{"nivel_urgencia_final": "RED"}', '{"nivel_urgencia_final": "ORANGE"}', '192.168.1.102', 'Streamlit/1.30');

-- =============================================
-- VERIFICACIÓN FINAL
-- =============================================
-- Mostrar resumen de datos cargados
DO $$
DECLARE
    user_count INTEGER;
    patient_count INTEGER;
    triage_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM usuarios;
    SELECT COUNT(*) INTO patient_count FROM pacientes;
    SELECT COUNT(*) INTO triage_count FROM triajes;
    
    RAISE NOTICE 'Base de datos inicializada con: % usuarios, % pacientes, % triajes', 
                  user_count, patient_count, triage_count;
END $$;