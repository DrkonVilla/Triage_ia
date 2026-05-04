-- =============================================
-- DATOS DE PRUEBA COMPLETOS - Sistema de Triaje IA
-- =============================================
-- Este archivo contiene inserciones masivas para todas las tablas

-- =============================================
-- 1. USUARIOS (Control de acceso)
-- =============================================
INSERT INTO usuarios (username, email, hashed_password, nombres, apellidos, rol, activo, last_login) VALUES
('gerente1', 'gerente1@hospital.com', '$2b$12$yourhashedpassword', 'Carlos', 'Martínez', 'gerente', TRUE, NOW() - INTERVAL '1 day'),
('enfermera1', 'enfermera1@hospital.com', '$2b$12$yourhashedpassword', 'María', 'López', 'enfermera', TRUE, NOW() - INTERVAL '2 hours'),
('enfermera2', 'enfermera2@hospital.com', '$2b$12$yourhashedpassword', 'Ana', 'García', 'enfermera', TRUE, NOW() - INTERVAL '5 hours'),
('enfermera3', 'enfermera3@hospital.com', '$2b$12$yourhashedpassword', 'Laura', 'Rodríguez', 'enfermera', TRUE, NOW() - INTERVAL '1 day'),
('medico1', 'medico1@hospital.com', '$2b$12$yourhashedpassword', 'Juan', 'Pérez', 'medico', TRUE, NOW() - INTERVAL '30 minutes'),
('medico2', 'medico2@hospital.com', '$2b$12$yourhashedpassword', 'Roberto', 'Sánchez', 'medico', TRUE, NOW() - INTERVAL '1 hour'),
('medico3', 'medico3@hospital.com', '$2b$12$yourhashedpassword', 'Diego', 'Fernández', 'medico', TRUE, NOW() - INTERVAL '3 hours'),
('auditor1', 'auditor1@hospital.com', '$2b$12$yourhashedpassword', 'Patricia', 'González', 'auditor', TRUE, NOW() - INTERVAL '1 week'),
('admin1', 'admin1@hospital.com', '$2b$12$yourhashedpassword', 'Luis', 'Ramírez', 'admin', TRUE, NOW()),
('enfermera4', 'enfermera4@hospital.com', '$2b$12$yourhashedpassword', 'Carmen', 'Torres', 'enfermera', TRUE, NOW() - INTERVAL '10 hours'),
('enfermera5', 'enfermera5@hospital.com', '$2b$12$yourhashedpassword', 'Sofía', 'Hernández', 'enfermera', TRUE, NOW() - INTERVAL '4 hours'),
('medico4', 'medico4@hospital.com', '$2b$12$yourhashedpassword', 'Alejandro', 'Ruiz', 'medico', TRUE, NOW() - INTERVAL '6 hours');

-- =============================================
-- 2. PACIENTES (50 pacientes variados)
-- =============================================
INSERT INTO pacientes (dni, nombres, apellidos, fecha_nacimiento, genero, telefono, email, direccion, activo) VALUES
('12345678', 'Juan', 'Martínez', '1985-03-15', 'M', '555-0101', 'juan.martinez@email.com', 'Av. Principal 123, Lima', TRUE),
('23456789', 'María', 'López', '1990-07-22', 'F', '555-0102', 'maria.lopez@email.com', 'Jr. Comercio 456, Lima', TRUE),
('34567890', 'Carlos', 'García', '1978-11-05', 'M', '555-0103', 'carlos.garcia@email.com', 'Calle Real 789, Lima', TRUE),
('45678901', 'Ana', 'Rodríguez', '1995-01-30', 'F', '555-0104', 'ana.rodriguez@email.com', 'Av. Las Flores 321, Lima', TRUE),
('56789012', 'Luis', 'Sánchez', '1982-09-12', 'M', '555-0105', 'luis.sanchez@email.com', 'Jr. París 654, Lima', TRUE),
('67890123', 'Carmen', 'Pérez', '1988-04-18', 'F', '555-0106', 'carmen.perez@email.com', 'Calle Lima 987, Lima', TRUE),
('78901234', 'Pedro', 'Fernández', '1975-12-25', 'M', '555-0107', 'pedro.fernandez@email.com', 'Av. Arequipa 147, Lima', TRUE),
('89012345', 'Sofía', 'González', '1992-06-08', 'F', '555-0108', 'sofia.gonzalez@email.com', 'Jr. Washington 258, Lima', TRUE),
('90123456', 'Miguel', 'Ramírez', '1980-02-14', 'M', '555-0109', 'miguel.ramirez@email.com', 'Calle Junín 369, Lima', TRUE),
('01234567', 'Laura', 'Torres', '1993-10-20', 'F', '555-0110', 'laura.torres@email.com', 'Av. Tacna 741, Lima', TRUE),
('11223344', 'Roberto', 'Vargas', '1968-08-03', 'M', '555-0111', 'roberto.vargas@email.com', 'Jr. Ica 852, Lima', TRUE),
('22334455', 'Diana', 'Castro', '1986-11-27', 'F', '555-0112', 'diana.castro@email.com', 'Calle Piura 963, Lima', TRUE),
('33445566', 'Jorge', 'Morales', '1979-05-16', 'M', '555-0113', 'jorge.morales@email.com', 'Av. Cusco 159, Lima', TRUE),
('44556677', 'Gabriela', 'Ortega', '1991-03-09', 'F', '555-0114', 'gabriela.ortega@email.com', 'Jr. Tumbes 357, Lima', TRUE),
('55667788', 'Fernando', 'Herrera', '1984-07-31', 'M', '555-0115', 'fernando.herrera@email.com', 'Calle Trujillo 486, Lima', TRUE),
('66778899', 'Patricia', 'Silva', '1977-01-23', 'F', '555-0116', 'patricia.silva@email.com', 'Av. Chiclayo 753, Lima', TRUE),
('77889900', 'Ricardo', 'Mendoza', '1994-09-05', 'M', '555-0117', 'ricardo.mendoza@email.com', 'Jr. Puno 951, Lima', TRUE),
('88990011', 'Isabel', 'Rojas', '1983-12-11', 'F', '555-0118', 'isabel.rojas@email.com', 'Calle Cajamarca 357, Lima', TRUE),
('99001122', 'Hugo', 'Guerrero', '1976-04-29', 'M', '555-0119', 'hugo.guerrero@email.com', 'Av. Loreto 159, Lima', TRUE),
('00112233', 'Monica', 'Cruz', '1989-08-17', 'F', '555-0120', 'monica.cruz@email.com', 'Jr. Ucayali 753, Lima', TRUE),
('12345001', 'Alejandro', 'Reyes', '1972-02-08', 'M', '555-0121', 'alejandro.reyes@email.com', 'Calle Amazonas 456, Lima', TRUE),
('23456002', 'Valentina', 'Navarro', '1996-06-25', 'F', '555-0122', 'valentina.navarro@email.com', 'Av. Madre de Dios 789, Lima', TRUE),
('34567003', 'Santiago', 'Aguirre', '1981-10-13', 'M', '555-0123', 'santiago.aguirre@email.com', 'Jr. San Martín 321, Lima', TRUE),
('45678004', 'Camila', 'Delgado', '1987-03-04', 'F', '555-0124', 'camila.delgado@email.com', 'Calle Huánuco 654, Lima', TRUE),
('56789005', 'Martín', 'Paredes', '1974-07-19', 'M', '555-0125', 'martin.paredes@email.com', 'Av. Pasco 987, Lima', TRUE),
('67890006', 'Luciana', 'Vega', '1990-11-22', 'F', '555-0126', 'luciana.vega@email.com', 'Jr. Huancavelica 147, Lima', TRUE),
('78901007', 'Emiliano', 'Flores', '1986-01-14', 'M', '555-0127', 'emiliano.flores@email.com', 'Calle Ayacucho 258, Lima', TRUE),
('89012008', 'Mariana', 'Espinoza', '1993-05-28', 'F', '555-0128', 'mariana.espinoza@email.com', 'Av. Apurímac 369, Lima', TRUE),
('90123009', 'Leonardo', 'Soto', '1978-09-10', 'M', '555-0129', 'leonardo.soto@email.com', 'Jr. Huancayo 741, Lima', TRUE),
('01234010', 'Victoria', 'Cáceres', '1985-12-02', 'F', '555-0130', 'victoria.caceres@email.com', 'Calle Huacho 852, Lima', TRUE),
('13579001', 'Andrés', 'Valenzuela', '1970-04-16', 'M', '555-0131', 'andres.valenzuela@email.com', 'Av. Chimbote 159, Lima', TRUE),
('24680002', 'Daniela', 'Bravo', '1997-08-24', 'F', '555-0132', 'daniela.bravo@email.com', 'Jr. Nazca 357, Lima', TRUE),
('35790003', 'Felipe', 'Araya', '1982-12-07', 'M', '555-0133', 'felipe.araya@email.com', 'Calle Iquitos 486, Lima', TRUE),
('46801004', 'Antonella', 'Peña', '1988-03-21', 'F', '555-0134', 'antonella.pena@email.com', 'Av. Pucallpa 753, Lima', TRUE),
('57912005', 'Maximiliano', 'Carrasco', '1975-06-14', 'M', '555-0135', 'maximiliano.carrasco@email.com', 'Jr. Tarapoto 951, Lima', TRUE),
('68023006', 'Julieta', 'Sandoval', '1992-10-09', 'F', '555-0136', 'julieta.sandoval@email.com', 'Calle Moyobamba 357, Lima', TRUE),
('79134007', 'Agustín', 'Tapia', '1980-02-27', 'M', '555-0137', 'agustin.tapia@email.com', 'Av. Yurimaguas 159, Lima', TRUE),
('80245008', 'Martina', 'Zúñiga', '1994-07-03', 'F', '555-0138', 'martina.zuniga@email.com', 'Jr. Jaén 753, Lima', TRUE),
('91356009', 'Benjamín', 'Contreras', '1973-11-18', 'M', '555-0139', 'benjamin.contreras@email.com', 'Calle Bagua 951, Lima', TRUE),
('02467010', 'Emilia', 'Figueroa', '1987-01-06', 'F', '555-0140', 'emilia.figueroa@email.com', 'Av. Bagua Grande 357, Lima', TRUE),
('13578111', 'Damián', 'Sepúlveda', '1998-05-11', 'M', '555-0141', 'damian.sepulveda@email.com', 'Jr. Chachapoyas 159, Lima', TRUE),
('24689222', 'Renata', 'Cárdenas', '1971-09-29', 'F', '555-0142', 'renata.cardenas@email.com', 'Calle Moyobamba 753, Lima', TRUE),
('35790333', 'Thiago', 'Salazar', '1984-02-02', 'M', '555-0143', 'thiago.salazar@email.com', 'Av. Rioja 951, Lima', TRUE),
('46801444', 'Olivia', 'Maldonado', '1995-06-17', 'F', '555-0144', 'olivia.maldonado@email.com', 'Jr. Lambayeque 357, Lima', TRUE),
('57912555', 'Benicio', 'Escobar', '1977-10-05', 'M', '555-0145', 'benicio.escobar@email.com', 'Calle Ferreñafe 159, Lima', TRUE),
('68023666', 'Alma', 'Palacios', '1991-12-23', 'F', '555-0146', 'alma.palacios@email.com', 'Jr. Chicama 753, Lima', TRUE),
('79134777', 'Bautista', 'Guzmán', '1969-08-12', 'M', '555-0147', 'bautista.guzman@email.com', 'Av. Virú 951, Lima', TRUE),
('80245888', 'Celeste', 'Escudero', '1983-04-01', 'F', '555-0148', 'celeste.escudero@email.com', 'Calle Guadalupe 357, Lima', TRUE),
('91356999', 'Ciro', 'Miranda', '1999-12-19', 'M', '555-0149', 'ciro.miranda@email.com', 'Jr. Chepén 159, Lima', TRUE);

-- =============================================
-- 3. CONTACTOS DE EMERGENCIA
-- =============================================
INSERT INTO contactos_emergencia (paciente_id, nombres_completos, telefono, parentesco) VALUES
(1, 'María Martínez', '555-0201', 'Esposa'),
(2, 'José López', '555-0202', 'Padre'),
(3, 'Carmen García', '555-0203', 'Esposa'),
(4, 'Roberto Rodríguez', '555-0204', 'Padre'),
(5, 'Diana Sánchez', '555-0205', 'Esposa'),
(6, 'Luis Pérez', '555-0206', 'Hermano'),
(7, 'Elena Fernández', '555-0207', 'Esposa'),
(8, 'Miguel González', '555-0208', 'Padre'),
(9, 'Ana Ramírez', '555-0209', 'Esposa'),
(10, 'Juan Torres', '555-0210', 'Padre'),
(11, 'Sofía Vargas', '555-0211', 'Esposa'),
(12, 'Carlos Castro', '555-0212', 'Hermano'),
(13, 'Patricia Morales', '555-0213', 'Esposa'),
(14, 'Diego Ortega', '555-0214', 'Padre'),
(15, 'Gabriela Herrera', '555-0215', 'Esposa'),
(16, 'Fernando Silva', '555-0216', 'Hermano'),
(17, 'Laura Mendoza', '555-0217', 'Esposa'),
(18, 'Santiago Rojas', '555-0218', 'Padre'),
(19, 'Isabel Guerrero', '555-0219', 'Esposa'),
(20, 'Emilio Cruz', '555-0220', 'Padre');

-- =============================================
-- 4. TRIAJES (80 triajes con diferentes estados y niveles de urgencia)
-- =============================================
INSERT INTO triajes (paciente_id, usuario_id, fecha_hora, motivo_consulta, nivel_urgencia_asignado_ia, nivel_urgencia_final, estado_logistico, notas_medicas, tiempo_atencion_segundos, activo) VALUES
-- Triajes del mes actual (variados)
(1, 2, NOW() - INTERVAL '2 hours', 'Dolor de pecho intenso', 'RED', 'RED', 'Atendido', 'Paciente con síntomas de infarto. Atención inmediata.', 480, TRUE),
(2, 3, NOW() - INTERVAL '3 hours', 'Fiebre alta y dolor de cabeza', 'YELLOW', 'YELLOW', 'Atendido', 'Fiebre 39°C. Administrado antipirético.', 900, TRUE),
(3, 2, NOW() - INTERVAL '4 hours', 'Dolor abdominal agudo', 'ORANGE', 'RED', 'Atendido', 'Apendicitis aguda. Derivado a cirugía.', 1200, TRUE),
(4, 4, NOW() - INTERVAL '5 hours', 'Tos y congestión nasal', 'GREEN', 'GREEN', 'Atendido', 'Resfriado común. Reposo indicado.', 600, TRUE),
(5, 3, NOW() - INTERVAL '6 hours', 'Fractura de brazo', 'YELLOW', 'YELLOW', 'Atendido', 'Fractura de cúbito. Yesado aplicado.', 1800, TRUE),
(6, 2, NOW() - INTERVAL '1 hour', 'Migraña severa', 'GREEN', 'YELLOW', 'En Atencion', 'Dolor craneal intenso. Analgésico administrado.', 720, TRUE),
(7, 4, NOW() - INTERVAL '30 minutes', 'Quemadura de segundo grado', 'YELLOW', 'YELLOW', 'En Atencion', 'Quemadura en antebrazo. Curación en proceso.', 900, TRUE),
(8, 3, NOW() - INTERVAL '45 minutes', 'Dificultad respiratoria', 'RED', 'RED', 'Llamado', 'Posible asma severo. Oxigenoterapia iniciada.', NULL, TRUE),
(9, 2, NOW() - INTERVAL '10 minutes', 'Corte en mano', 'BLUE', 'GREEN', 'En Espera', 'Laceración superficial. Esperando curación.', NULL, TRUE),
(10, 4, NOW() - INTERVAL '15 minutes', 'Náuseas y vómitos', 'GREEN', 'GREEN', 'En Espera', 'Gastroenteritis probable. Hidratación oral.', NULL, TRUE),

-- Triajes de febrero 2024
(11, 2, '2024-02-15 14:30:00', 'Dolor torácico', 'RED', 'RED', 'Atendido', 'Infarto agudo al miocardio. Trombolisis aplicada.', 420, TRUE),
(12, 3, '2024-02-14 09:15:00', 'Dolor de garganta', 'GREEN', 'GREEN', 'Atendido', 'Faringitis estreptocócica. Antibiótico prescrito.', 540, TRUE),
(13, 4, '2024-02-13 16:45:00', 'Trauma craneoencefálico', 'RED', 'RED', 'Atendido', 'Accidente de tráfico. TAC realizado.', 1800, TRUE),
(14, 2, '2024-02-12 11:20:00', 'Dolor lumbar', 'YELLOW', 'GREEN', 'Atendido', 'Lumbalgia aguda. AINEs indicados.', 780, TRUE),
(15, 3, '2024-02-11 08:00:00', 'Hemorragia nasal', 'ORANGE', 'YELLOW', 'Atendido', 'Epistaxis. Tamponado anterior realizado.', 660, TRUE),
(16, 4, '2024-02-10 19:30:00', 'Alergia alimentaria', 'YELLOW', 'YELLOW', 'Atendido', 'Shock anafiláctico. Adrenalina administrada.', 480, TRUE),
(17, 2, '2024-02-09 13:45:00', 'Dolor de oído', 'BLUE', 'GREEN', 'Atendido', 'Otitis media. Antibiótico tópico indicado.', 600, TRUE),
(18, 3, '2024-02-08 10:00:00', 'Convulsiones', 'RED', 'RED', 'Atendido', 'Crisis epiléptica. Diazepam IV administrado.', 900, TRUE),
(19, 4, '2024-02-07 15:20:00', 'Dolor articular', 'GREEN', 'GREEN', 'Atendido', 'Artritis reumatoide. AINEs indicados.', 720, TRUE),
(20, 2, '2024-02-06 07:45:00', 'Hemoptisis', 'ORANGE', 'ORANGE', 'Atendido', 'Tuberculosis sospechada. Aislamiento indicado.', 1200, TRUE),

-- Triajes de enero 2024
(21, 3, '2024-01-25 12:00:00', 'Síncope', 'ORANGE', 'ORANGE', 'Atendido', 'Pérdida de conciencia breve. Estudio cardiológico.', 840, TRUE),
(22, 2, '2024-01-24 18:30:00', 'Herida de bala', 'RED', 'RED', 'Atendido', 'Trauma penetrante. Cirugía de emergencia.', 3600, TRUE),
(23, 4, '2024-01-23 09:00:00', 'Infección urinaria', 'YELLOW', 'YELLOW', 'Atendido', 'Cistitis. Antibiótico oral prescrito.', 540, TRUE),
(24, 3, '2024-01-22 14:15:00', 'Dolor ocular', 'YELLOW', 'YELLOW', 'Atendido', 'Uveítis. Derivar a oftalmología.', 660, TRUE),
(25, 2, '2024-01-21 11:00:00', 'Palpitaciones', 'YELLOW', 'ORANGE', 'Atendido', 'Arritmia supraventricular. ECG anormal.', 780, TRUE),
(26, 4, '2024-01-20 16:45:00', 'Esguince de tobillo', 'GREEN', 'GREEN', 'Atendido', 'Trauma leve. Vendaje compresivo.', 600, TRUE),
(27, 3, '2024-01-19 08:30:00', 'Dolor abdominal difuso', 'YELLOW', 'YELLOW', 'Atendido', 'Gastroenteritis. Hidratación IV.', 900, TRUE),
(28, 2, '2024-01-18 20:00:00', 'Cefalea explosiva', 'RED', 'RED', 'Atendido', 'Hemorragia subaracnoidea. TAC urgente.', 1500, TRUE),
(29, 4, '2024-01-17 10:30:00', 'Erupción cutánea', 'GREEN', 'GREEN', 'Atendido', 'Dermatitis alérgica. Antihistamínico.', 480, TRUE),
(30, 3, '2024-01-16 13:00:00', 'Dolor torácico pleurítico', 'ORANGE', 'ORANGE', 'Atendido', 'Neumotórax. Drenaje torácico.', 2100, TRUE),

-- Triajes de diciembre 2023
(31, 2, '2023-12-28 15:30:00', 'Intoxicación alimentaria', 'GREEN', 'GREEN', 'Atendido', 'Vómitos y diarrea. Hidratación.', 720, TRUE),
(32, 3, '2023-12-27 09:45:00', 'Dolor de espalda', 'BLUE', 'GREEN', 'Atendido', 'Contractura muscular. Fisioterapia indicada.', 540, TRUE),
(33, 4, '2023-12-26 11:20:00', 'Cuerpo extraño en ojo', 'YELLOW', 'YELLOW', 'Atendido', 'Extracción de cuerpo extraño. Antibiótico.', 480, TRUE),
(34, 2, '2023-12-25 19:00:00', 'Quemadura eléctrica', 'RED', 'RED', 'Atendido', 'Electrocución. Monitorización cardiaca.', 1800, TRUE),
(35, 3, '2023-12-24 14:00:00', 'Bronquitis aguda', 'YELLOW', 'YELLOW', 'Atendido', 'Broncoespasmo. Broncodilatadores.', 840, TRUE),
(36, 4, '2023-12-23 10:15:00', 'Dolor dental', 'BLUE', 'BLUE', 'Atendido', 'Absceso dental. Antibiótico + analgésico.', 360, TRUE),
(37, 2, '2023-12-22 17:30:00', 'Hipotermia', 'ORANGE', 'ORANGE', 'Atendido', 'Exposición al frío. Reanimación.', 1200, TRUE),
(38, 3, '2023-12-21 08:00:00', 'Cálculo renal', 'YELLOW', 'YELLOW', 'Atendido', 'Colico nefrítico. AINEs + espasmolíticos.', 1800, TRUE),
(39, 4, '2023-12-20 13:45:00', 'Insomnio crónico', 'BLUE', 'BLUE', 'Atendido', 'Trastorno del sueño. Derivado a psiquiatría.', 420, TRUE),
(40, 2, '2023-12-19 16:00:00', 'Amputación parcial', 'RED', 'RED', 'Atendido', 'Trauma laboral. Reimplante no viable.', 2400, TRUE),

-- Triajes de noviembre 2023
(41, 3, '2023-11-30 12:30:00', 'Neumonía', 'ORANGE', 'ORANGE', 'Atendido', 'Consolidación pulmonar. Antibiótico IV.', 1500, TRUE),
(42, 4, '2023-11-29 09:00:00', 'Mareos', 'GREEN', 'GREEN', 'Atendido', 'Vértigo posicional. Maniobras de Epley.', 600, TRUE),
(43, 2, '2023-11-28 15:00:00', 'Herida punzante', 'YELLOW', 'YELLOW', 'Atendido', 'Laceración. Sutura realizada.', 720, TRUE),
(44, 3, '2023-11-27 11:45:00', 'Déficit neurológico', 'RED', 'RED', 'Atendido', 'Accidente vascular isquémico. Trombolisis.', 2700, TRUE),
(45, 4, '2023-11-26 14:30:00', 'Conjuntivitis', 'BLUE', 'BLUE', 'Atendido', 'Infección viral. Higiene ocular.', 420, TRUE),
(46, 2, '2023-11-25 18:00:00', 'Dolor precordial', 'RED', 'ORANGE', 'Atendido', 'Angina inestable. Estudio hemodinámico.', 1200, TRUE),
(47, 3, '2023-11-24 10:30:00', 'Gota', 'YELLOW', 'YELLOW', 'Atendido', 'Artritis gotosa. Colchicina indicada.', 660, TRUE),
(48, 4, '2023-11-23 16:15:00', 'Ansiedad aguda', 'YELLOW', 'GREEN', 'Atendido', 'Crisis de pánico. Ansiolítico.', 540, TRUE),
(49, 2, '2023-11-22 08:45:00', 'Hematemesis', 'RED', 'RED', 'Atendido', 'Úlcera sangrante. Endoscopia urgente.', 1800, TRUE),
(50, 3, '2023-11-21 13:30:00', 'Faringitis', 'GREEN', 'GREEN', 'Atendido', 'Infección viral. Sintomático.', 480, TRUE),

-- Más triajes para volumen
(1, 5, '2024-02-16 10:00:00', 'Dolor torácico irradiado', 'RED', 'RED', 'Atendido', 'Angina de pecho. Nitratos administrados.', 600, TRUE),
(2, 6, '2024-02-17 14:20:00', 'Gripe estacional', 'GREEN', 'GREEN', 'Atendido', 'Influenza A. Antiviral oseltamivir.', 480, TRUE),
(3, 5, '2024-02-18 09:45:00', 'Apendicitis', 'RED', 'RED', 'Atendido', 'Peritonitis localizada. Apendicectomía.', 2400, TRUE),
(4, 6, '2024-02-19 16:30:00', 'Esguince cervical', 'YELLOW', 'YELLOW', 'Atendido', 'Trauma cervical. Collarín cervical.', 720, TRUE),
(5, 5, '2024-02-20 11:15:00', 'Pielonefritis', 'ORANGE', 'ORANGE', 'Atendido', 'Infección renal ascendente. Antibiótico IV.', 1500, TRUE),
(6, 6, '2024-02-21 08:00:00', 'Vértigo', 'YELLOW', 'YELLOW', 'Atendido', 'Enfermedad de Meniere. Betahistina.', 660, TRUE),
(7, 5, '2024-02-22 19:45:00', 'Trauma facial', 'YELLOW', 'YELLOW', 'Atendido', 'Fractura nasal. Reposición manual.', 900, TRUE),
(8, 6, '2024-02-23 12:00:00', 'Dengue', 'ORANGE', 'ORANGE', 'Atendido', 'Fiebre hemorrágica. Hidratación agresiva.', 1800, TRUE),
(9, 5, '2024-02-24 07:30:00', 'Colecistitis', 'YELLOW', 'YELLOW', 'Atendido', 'Cálculos biliares. Electivo quirúrgico.', 1200, TRUE),
(10, 6, '2024-02-25 15:00:00', 'Meningitis', 'RED', 'RED', 'Atendido', 'Cefalea y rigidez de nuca. Ceftriaxona IV.', 3600, TRUE);

-- =============================================
-- 5. SIGNOS VITALES (para cada triaje completado)
-- =============================================
INSERT INTO signos_vitales (triaje_id, presion_sistolica, presion_diastolica, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, saturacion_o2, nota_suplementaria) VALUES
(1, 180, 110, 110, 24, 37.2, 95, 'Hipertensión severa. Controlar PA.'),
(2, 130, 85, 95, 20, 39.1, 98, 'Fiebre alta.'),
(3, 140, 90, 105, 22, 38.0, 97, 'Dolor abdominal.'),
(4, 120, 80, 75, 18, 37.0, 99, 'Estable.'),
(5, 125, 82, 88, 19, 36.8, 100, 'Dolor moderado.'),
(6, 118, 78, 72, 16, 36.5, 99, 'Dolor craneal.'),
(7, 128, 84, 92, 20, 37.1, 98, 'Quemadura.'),
(8, 110, 75, 115, 28, 37.0, 88, 'Dificultad respiratoria.'),
(9, 122, 80, 70, 18, 36.7, 100, 'Lesión leve.'),
(10, 124, 82, 78, 19, 37.2, 99, 'Deshidratación leve.'),
(11, 160, 100, 105, 22, 37.0, 94, 'Infarto.'),
(12, 118, 76, 82, 18, 37.5, 99, 'Faringitis.'),
(13, 90, 60, 120, 25, 36.0, 92, 'Trauma craneal.'),
(14, 128, 82, 78, 18, 36.8, 98, 'Dolor lumbar.'),
(15, 135, 88, 95, 20, 37.0, 97, 'Epistaxis.'),
(16, 85, 55, 115, 24, 36.5, 93, 'Anafilaxia.'),
(17, 120, 78, 72, 18, 37.2, 99, 'Otitis.'),
(18, 140, 90, 125, 22, 38.5, 96, 'Convulsiones.'),
(19, 132, 86, 80, 19, 36.9, 98, 'Artritis.'),
(20, 145, 92, 100, 24, 37.8, 95, 'Hemoptisis.'),
(21, 110, 70, 95, 20, 36.5, 97, 'Síncope.'),
(22, 80, 50, 130, 30, 35.0, 85, 'Shock hemorrágico.'),
(23, 125, 80, 88, 19, 37.6, 99, 'Infección urinaria.'),
(24, 120, 78, 76, 18, 36.8, 100, 'Dolor ocular.'),
(25, 138, 88, 110, 22, 37.1, 97, 'Arritmia.'),
(26, 122, 80, 70, 18, 36.5, 100, 'Trauma leve.'),
(27, 118, 76, 85, 20, 37.4, 98, 'Gastroenteritis.'),
(28, 175, 105, 115, 24, 37.0, 94, 'Hemorragia cerebral.'),
(29, 120, 78, 74, 18, 37.0, 99, 'Alergia.'),
(30, 140, 90, 105, 26, 37.2, 91, 'Neumotórax.'),
(31, 110, 72, 88, 20, 37.8, 98, 'Intoxicación.'),
(32, 115, 75, 70, 16, 36.5, 99, 'Contractura.'),
(33, 125, 82, 78, 18, 37.0, 100, 'Trauma ocular.'),
(34, 135, 88, 125, 28, 36.0, 90, 'Electrocución.'),
(35, 118, 78, 95, 24, 37.5, 96, 'Bronquitis.'),
(36, 120, 80, 72, 18, 37.0, 99, 'Dolor dental.'),
(37, 95, 60, 55, 12, 33.0, 92, 'Hipotermia.'),
(38, 128, 85, 100, 22, 38.0, 97, 'Cálculo renal.'),
(39, 122, 78, 68, 16, 36.5, 99, 'Insomnio.'),
(40, 70, 45, 140, 32, 35.5, 88, 'Shock traumático.'),
(41, 145, 95, 110, 26, 38.5, 92, 'Neumonía.'),
(42, 120, 78, 75, 18, 36.8, 99, 'Mareo.'),
(43, 118, 76, 82, 19, 36.9, 98, 'Herida.'),
(44, 150, 95, 130, 24, 37.0, 90, 'ACV.'),
(45, 115, 75, 70, 18, 37.0, 100, 'Conjuntivitis.'),
(46, 165, 105, 108, 22, 37.0, 95, 'Angina.'),
(47, 138, 90, 88, 20, 37.5, 98, 'Gota.'),
(48, 128, 82, 95, 20, 37.2, 99, 'Ansiedad.'),
(49, 100, 65, 115, 24, 36.8, 89, 'Hemorragia GI.'),
(50, 122, 80, 76, 18, 37.4, 99, 'Faringitis.'),
(51, 170, 105, 105, 22, 37.0, 94, 'Angina.'),
(52, 118, 76, 82, 18, 38.0, 99, 'Gripe.'),
(53, 140, 90, 110, 24, 38.5, 96, 'Peritonitis.'),
(54, 125, 82, 85, 20, 37.0, 98, 'Trauma.'),
(55, 148, 95, 105, 22, 38.2, 95, 'Pielonefritis.'),
(56, 128, 82, 78, 18, 36.9, 99, 'Vértigo.'),
(57, 122, 80, 88, 19, 37.1, 98, 'Trauma facial.'),
(58, 135, 88, 115, 24, 38.8, 92, 'Dengue.'),
(59, 130, 85, 90, 20, 37.6, 97, 'Colecistitis.'),
(60, 110, 70, 125, 26, 38.5, 93, 'Meningitis.');

-- =============================================
-- 6. SÍNTOMAS DE TRIAJE (síntomas por cada caso)
-- =============================================
INSERT INTO sintomas_triaje (triaje_id, sintoma, intensidad, descripcion_libre) VALUES
(1, 'Dolor torácico', 'Grave', 'Oprimido, irradia a brazo izquierdo'),
(1, 'Sudoración', 'Moderado', 'Sudoración profusa'),
(1, 'Náuseas', 'Leve', NULL),
(2, 'Fiebre', 'Moderado', '39°C desde hace 2 días'),
(2, 'Dolor de cabeza', 'Moderado', 'Frontal y constante'),
(2, 'Malestar general', 'Moderado', NULL),
(3, 'Dolor abdominal', 'Grave', 'Fosa ilíaca derecha'),
(3, 'Vómitos', 'Moderado', 'Alimentarios'),
(3, 'Fiebre', 'Leve', '37.8°C'),
(4, 'Tos', 'Leve', 'Productiva'),
(4, 'Congestión nasal', 'Leve', NULL),
(4, 'Estornudos', 'Leve', NULL),
(5, 'Dolor', 'Grave', 'Intenso en antebrazo'),
(5, 'Deformidad', 'Moderado', 'Angulación visible'),
(6, 'Dolor de cabeza', 'Grave', 'Pulsátil unilateral'),
(6, 'Fotofobia', 'Moderado', 'Intolerancia a la luz'),
(6, 'Náuseas', 'Leve', NULL),
(8, 'Disnea', 'Grave', 'Dificultad para respirar'),
(8, 'Sibilancias', 'Moderado', 'Al espirar'),
(8, 'Tos', 'Leve', 'Seca'),
(11, 'Dolor torácico', 'Grave', 'Tipo opresivo'),
(11, 'Sudoración', 'Moderado', NULL),
(11, 'Disnea', 'Moderado', 'Leve al esfuerzo'),
(13, 'Alteración conciencia', 'Grave', 'Glasgow 12'),
(13, 'Dolor de cabeza', 'Grave', 'Intenso'),
(14, 'Dolor lumbar', 'Moderado', 'Irradia a glúteo'),
(18, 'Convulsiones', 'Grave', 'Tónico-clónicas generalizadas'),
(18, 'Alteración conciencia', 'Grave', 'Post-ictal'),
(22, 'Dolor', 'Grave', 'Herida de bala en abdomen'),
(22, 'Hemorragia', 'Grave', 'Activa'),
(28, 'Cefalea explosiva', 'Grave', 'Peor dolor de su vida'),
(28, 'Rigidez de nuca', 'Grave', NULL),
(30, 'Dolor torácico', 'Grave', 'Pleurítico'),
(30, 'Disnea', 'Grave', 'Repentina'),
(34, 'Quemadura', 'Grave', 'Entrada y salida'),
(34, 'Arritmia', 'Grave', 'Fibrilación ventricular'),
(40, 'Amputación', 'Grave', 'Dedos de mano derecha'),
(44, 'Déficit motor', 'Grave', 'Hemiplejia izquierda'),
(44, 'Afasia', 'Grave', 'Expresiva'),
(49, 'Vómito sanguinolento', 'Grave', 'Café en grano'),
(49, 'Melenas', 'Grave', 'Evacuación negra'),
(53, 'Dolor abdominal', 'Grave', 'McBurny positivo'),
(53, 'Rebound', 'Grave', 'Positivo'),
(58, 'Fiebre', 'Grave', '40°C'),
(58, 'Dolor retroocular', 'Grave', NULL),
(58, 'Rash', 'Moderado', 'Petequial'),
(60, 'Cefalea', 'Grave', 'Intensidad máxima'),
(60, 'Fiebre', 'Grave', '39.5°C'),
(60, 'Rigidez de nuca', 'Grave', 'Brudzinski positivo');

-- =============================================
-- 7. RESULTADOS IA (resultados del modelo para algunos casos)
-- =============================================
INSERT INTO resultados_ia (triaje_id, prompt_enviado, respuesta_raw_llm, diagnosticos_json, recomendaciones_json, modelo_utilizado, latencia_segundos) VALUES
(1, 'Prompt: Paciente masculino 38 años, dolor de pecho intenso...', 'RESPONSE: Nivel RED - Probable síndrome coronario agudo. Recomendación: ECG inmediato, troponinas, nitroglicerina.', '[{"diagnostico": "Síndrome coronario agudo", "probabilidad": 0.85}]'::jsonb, '[{"accion": "ECG 12 derivaciones", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.5),
(2, 'Prompt: Paciente femenina 33 años, fiebre alta y dolor de cabeza...', 'RESPONSE: Nivel YELLOW - Posible infección viral. Recomendación: Antipiréticos, hidratación.', '[{"diagnostico": "Infección viral", "probabilidad": 0.75}]'::jsonb, '[{"accion": "Paracetamol 1g", "prioridad": "estándar"}]'::jsonb, 'gpt-4', 1.8),
(3, 'Prompt: Paciente masculino 45 años, dolor abdominal agudo...', 'RESPONSE: Nivel RED - Apendicitis aguda probable. Recomendación: Evaluación quirúrgica urgente.', '[{"diagnostico": "Apendicitis aguda", "probabilidad": 0.80}]'::jsonb, '[{"accion": "Cirugía de emergencia", "prioridad": "urgente"}]'::jsonb, 'gpt-4', 2.2),
(11, 'Prompt: Paciente masculino 55 años, dolor torácico...', 'RESPONSE: Nivel RED - Infarto agudo al miocardio. Recomendación: Activar código infarto.', '[{"diagnostico": "IAM", "probabilidad": 0.90}]'::jsonb, '[{"accion": "Trombolisis", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.1),
(13, 'Prompt: Paciente masculino 45 años, trauma craneoencefálico...', 'RESPONSE: Nivel RED - Trauma craneal severo. Recomendación: TAC urgente, neurocirugía.', '[{"diagnostico": "TCE severo", "probabilidad": 0.88}]'::jsonb, '[{"accion": "TAC craneo", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.8),
(18, 'Prompt: Paciente masculino 44 años, convulsiones...', 'RESPONSE: Nivel RED - Crisis convulsiva generalizada. Recomendación: Diazepam IV, protección vía aérea.', '[{"diagnostico": "Crisis epiléptica", "probabilidad": 0.92}]'::jsonb, '[{"accion": "Diazepam 10mg IV", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 1.9),
(22, 'Prompt: Paciente masculino 46 años, herida de bala...', 'RESPONSE: Nivel RED - Trauma penetrante abdomen. Recomendación: Cirugía exploradora urgente.', '[{"diagnostico": "Trauma penetrante", "probabilidad": 0.95}]'::jsonb, '[{"accion": "Laparotomía", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.3),
(28, 'Prompt: Paciente femenina 31 años, cefalea explosiva...', 'RESPONSE: Nivel RED - Hemorragia subaracnoidea. Recomendación: TAC, neurocirugía.', '[{"diagnostico": "HSA", "probabilidad": 0.87}]'::jsonb, '[{"accion": "TAC urgente", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.0),
(44, 'Prompt: Paciente femenina 37 años, déficit neurológico...', 'RESPONSE: Nivel RED - Accidente vascular isquémico. Recomendación: Ventana terapéutica trombolisis.', '[{"diagnostico": "ACV isquémico", "probabilidad": 0.91}]'::jsonb, '[{"accion": "Trombolisis IV", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.4),
(49, 'Prompt: Paciente masculino 48 años, vómito sanguinolento...', 'RESPONSE: Nivel RED - Hemorragia digestiva alta. Recomendación: Endoscopia urgente.', '[{"diagnostico": "Hemorragia GI", "probabilidad": 0.89}]'::jsonb, '[{"accion": "Endoscopia", "prioridad": "urgente"}]'::jsonb, 'gpt-4', 2.1);

-- =============================================
-- 8. HCE - ANTECEDENTES (historia clínica)
-- =============================================
INSERT INTO hce_antecedentes (paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo) VALUES
(1, 'Patologia', 'Hipertensión arterial', 'HTA diagnosticada hace 5 años', '2019-03-15', TRUE),
(1, 'Medicamento', 'Losartán', '50mg diario', '2019-03-15', TRUE),
(1, 'Alergia', 'Penicilina', 'Urticaria', '2010-06-20', TRUE),
(3, 'Patologia', 'Diabetes mellitus tipo 2', 'DM2 diagnosticada 2020', '2020-11-10', TRUE),
(3, 'Medicamento', 'Metformina', '850mg cada 12 horas', '2020-11-10', TRUE),
(5, 'Patologia', 'Asma', 'Asma moderada persistente', '2015-08-05', TRUE),
(5, 'Medicamento', 'Salbutamol', 'Inhalador de rescate', '2015-08-05', TRUE),
(8, 'Patologia', 'Epilepsia', 'Desde adolescencia', '2008-03-12', TRUE),
(8, 'Medicamento', 'Ácido valproico', '500mg cada 12 horas', '2008-03-12', TRUE),
(11, 'Patologia', 'Dislipidemia', 'Colesterol elevado', '2018-01-20', TRUE),
(11, 'Medicamento', 'Atorvastatina', '20mg nocte', '2018-01-20', TRUE),
(13, 'Cirugia', 'Apendicectomía', 'Cirugía laparoscópica', '2015-07-10', FALSE),
(17, 'Alergia', 'Yodo', 'Reacción cutánea', '2012-09-15', TRUE),
(19, 'Patologia', 'Artritis reumatoide', 'Diagnosticada 2019', '2019-04-22', TRUE),
(19, 'Medicamento', 'Metotrexate', '15mg semanal', '2019-04-22', TRUE),
(25, 'Patologia', 'Arritmia', 'FA paroxística', '2020-02-14', TRUE),
(28, 'Alergia', 'Látex', 'Anafilaxia leve', '2015-12-03', TRUE),
(31, 'Patologia', 'EPOC', 'Enfermedad pulmonar crónica', '2017-11-18', TRUE),
(35, 'Patologia', 'Bronquitis crónica', 'Fumador ex 20 paquetes-año', '2016-09-25', TRUE),
(38, 'Cirugia', 'Colecistectomía', 'Por colelitiasis', '2010-05-15', FALSE);

-- =============================================
-- 9. HCE - CONSULTAS PREVIAS
-- =============================================
INSERT INTO hce_consulta_previa (paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento) VALUES
(1, '2023-08-15 09:00:00', 'Control de hipertensión', 'HTA compensada', 'Continuar Losartán 50mg'),
(1, '2023-12-10 10:30:00', 'Dolor de espalda', 'Lumbalgia aguda', 'AINEs por 7 días'),
(3, '2023-06-20 14:00:00', 'Control DM2', 'DM2 compensada HbA1c 7.2%', 'Continuar Metformina'),
(3, '2023-11-05 09:30:00', 'Infección respiratoria', 'Faringitis aguda', 'Amoxicilina 7 días'),
(5, '2023-09-12 11:00:00', 'Exacerbación asmática', 'Asma moderada', 'Prednisona 5 días'),
(8, '2023-07-25 16:00:00', 'Control epilepsia', 'Epilepsia estable', 'Continuar valproato'),
(11, '2023-10-08 10:00:00', 'Control dislipidemia', 'Dislipidemia mejorada', 'Continuar estatina'),
(19, '2023-05-18 09:15:00', 'Control artritis', 'AR actividad moderada', 'Ajustar MTX'),
(25, '2023-08-22 14:30:00', 'Palpitaciones', 'FA paroxística', 'Anticoagulante iniciado'),
(31, '2023-09-30 11:45:00', 'Exacerbación EPOC', 'EPOC exacerbada', 'Corticoides + antibiótico');

-- =============================================
-- 10. LOGS DE AUDITORÍA
-- =============================================
INSERT INTO logs_auditoria (usuario_id, accion, modulo, registro_id, datos_anteriores, datos_nuevos, ip_address, user_agent, timestamp) VALUES
(2, 'INSERT', 'triajes', 1, NULL, '{"paciente_id": 1, "nivel": "RED"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '2 hours'),
(2, 'UPDATE', 'triajes', 1, '{"estado": "En Espera"}'::jsonb, '{"estado": "En Atencion"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '1 hour 30 minutes'),
(2, 'UPDATE', 'triajes', 1, '{"estado": "En Atencion"}'::jsonb, '{"estado": "Atendido"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '30 minutes'),
(3, 'INSERT', 'triajes', 2, NULL, '{"paciente_id": 2, "nivel": "YELLOW"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '3 hours'),
(3, 'UPDATE', 'triajes', 2, '{"nivel_ia": "RED", "nivel_final": null}'::jsonb, '{"nivel_ia": "RED", "nivel_final": "YELLOW"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '2 hours 30 minutes'),
(4, 'INSERT', 'triajes', 4, NULL, '{"paciente_id": 4, "nivel": "GREEN"}'::jsonb, '192.168.1.12'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '5 hours'),
(4, 'INSERT', 'signos_vitales', 4, NULL, '{"triaje_id": 4, "fc": 75}'::jsonb, '192.168.1.12'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '4 hours 45 minutes'),
(5, 'INSERT', 'triajes', 51, NULL, '{"paciente_id": 1, "nivel": "RED"}'::jsonb, '192.168.1.15'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2024-02-16 10:00:00'),
(6, 'INSERT', 'triajes', 52, NULL, '{"paciente_id": 2, "nivel": "GREEN"}'::jsonb, '192.168.1.16'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2024-02-17 14:20:00'),
(2, 'STATUS_CHANGE', 'triajes', 8, '{"estado": "En Espera"}'::jsonb, '{"estado": "Llamado"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '20 minutes'),
(3, 'STATUS_CHANGE', 'triajes', 8, '{"estado": "Llamado"}'::jsonb, '{"estado": "En Atencion"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '5 minutes'),
(8, 'INSERT', 'triajes', 8, NULL, '{"paciente_id": 8, "nivel": "RED"}'::jsonb, '192.168.1.20'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '45 minutes'),
(9, 'INSERT', 'triajes', 9, NULL, '{"paciente_id": 9, "nivel": "GREEN"}'::jsonb, '192.168.1.21'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', NOW() - INTERVAL '10 minutes'),
(1, 'INSERT', 'triajes', 60, NULL, '{"paciente_id": 10, "nivel": "RED"}'::jsonb, '192.168.1.50'::inet, 'PostmanRuntime/7.36.0', '2024-02-25 15:00:00'),
(7, 'INSERT', 'triajes', 53, NULL, '{"paciente_id": 3, "nivel": "RED"}'::jsonb, '192.168.1.17'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2024-02-18 09:45:00'),
(7, 'UPDATE', 'triajes', 53, '{"estado": "En Espera"}'::jsonb, '{"estado": "Atendido"}'::jsonb, '192.168.1.17'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2024-02-18 10:45:00'),
(8, 'DELETE', 'triajes', 100, '{"paciente_id": 15}'::jsonb, NULL, '192.168.1.18'::inet, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2023-12-15 09:00:00');

-- =============================================
-- FIN DEL ARCHIVO DE DATOS
-- =============================================
