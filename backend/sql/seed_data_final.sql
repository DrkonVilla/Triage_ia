-- =============================================
-- DATOS DE PRUEBA - Sistema de Triaje IA
-- =============================================

-- Desactivar constraints
SET session_replication_role = 'replica';

-- Truncar tablas
TRUNCATE TABLE logs_auditoria, hce_consulta_previa, hce_antecedentes, 
              resultados_ia, sintomas_triaje, signos_vitales, 
              triajes, contactos_emergencia, pacientes, usuarios 
RESTART IDENTITY CASCADE;

-- Reactivar constraints
SET session_replication_role = 'origin';

-- =============================================
-- 1. USUARIOS (12 usuarios)
-- =============================================
INSERT INTO usuarios (id, username, email, hashed_password, nombres, apellidos, rol, activo, last_login) VALUES
(1, 'gerente1', 'gerente1@hospital.com', '$2b$12$yourhashedpassword', 'Carlos', 'Martinez', 'gerente', TRUE, NOW() - INTERVAL '1 day'),
(2, 'enfermera1', 'enfermera1@hospital.com', '$2b$12$yourhashedpassword', 'Maria', 'Lopez', 'enfermera', TRUE, NOW() - INTERVAL '2 hours'),
(3, 'enfermera2', 'enfermera2@hospital.com', '$2b$12$yourhashedpassword', 'Ana', 'Garcia', 'enfermera', TRUE, NOW() - INTERVAL '5 hours'),
(4, 'medico1', 'medico1@hospital.com', '$2b$12$yourhashedpassword', 'Juan', 'Perez', 'medico', TRUE, NOW() - INTERVAL '30 minutes'),
(5, 'auditor1', 'auditor1@hospital.com', '$2b$12$yourhashedpassword', 'Patricia', 'Gonzalez', 'auditor', TRUE, NOW() - INTERVAL '1 week'),
(6, 'medico2', 'medico2@hospital.com', '$2b$12$yourhashedpassword', 'Roberto', 'Sanchez', 'medico', TRUE, NOW() - INTERVAL '1 hour'),
(7, 'enfermera3', 'enfermera3@hospital.com', '$2b$12$yourhashedpassword', 'Laura', 'Rodriguez', 'enfermera', TRUE, NOW() - INTERVAL '1 day'),
(8, 'medico3', 'medico3@hospital.com', '$2b$12$yourhashedpassword', 'Diego', 'Fernandez', 'medico', TRUE, NOW() - INTERVAL '3 hours'),
(9, 'enfermera4', 'enfermera4@hospital.com', '$2b$12$yourhashedpassword', 'Carmen', 'Torres', 'enfermera', TRUE, NOW() - INTERVAL '10 hours'),
(10, 'enfermera5', 'enfermera5@hospital.com', '$2b$12$yourhashedpassword', 'Sofia', 'Hernandez', 'enfermera', TRUE, NOW() - INTERVAL '4 hours'),
(11, 'medico4', 'medico4@hospital.com', '$2b$12$yourhashedpassword', 'Alejandro', 'Ruiz', 'medico', TRUE, NOW() - INTERVAL '6 hours'),
(12, 'enfermera6', 'enfermera6@hospital.com', '$2b$12$yourhashedpassword', 'Isabel', 'Rojas', 'enfermera', TRUE, NOW() - INTERVAL '8 hours');

SELECT setval('usuarios_id_seq', 12);

-- =============================================
-- 2. PACIENTES (50 pacientes, IDs 1-50)
-- =============================================
INSERT INTO pacientes (id, dni, nombres, apellidos, fecha_nacimiento, genero, telefono, email, direccion, activo) VALUES
(1, '12345678', 'Juan', 'Martinez', '1985-03-15', 'M', '555-0101', 'juan.martinez@email.com', 'Av. Principal 123, Lima', TRUE),
(2, '23456789', 'Maria', 'Lopez', '1990-07-22', 'F', '555-0102', 'maria.lopez@email.com', 'Jr. Comercio 456, Lima', TRUE),
(3, '34567890', 'Carlos', 'Garcia', '1978-11-05', 'M', '555-0103', 'carlos.garcia@email.com', 'Calle Real 789, Lima', TRUE),
(4, '45678901', 'Ana', 'Rodriguez', '1995-01-30', 'F', '555-0104', 'ana.rodriguez@email.com', 'Av. Las Flores 321, Lima', TRUE),
(5, '56789012', 'Luis', 'Sanchez', '1982-09-12', 'M', '555-0105', 'luis.sanchez@email.com', 'Jr. Paris 654, Lima', TRUE),
(6, '67890123', 'Carmen', 'Perez', '1988-04-18', 'F', '555-0106', 'carmen.perez@email.com', 'Calle Lima 987, Lima', TRUE),
(7, '78901234', 'Pedro', 'Fernandez', '1975-12-25', 'M', '555-0107', 'pedro.fernandez@email.com', 'Av. Arequipa 147, Lima', TRUE),
(8, '89012345', 'Sofia', 'Gonzalez', '1992-06-08', 'F', '555-0108', 'sofia.gonzalez@email.com', 'Jr. Washington 258, Lima', TRUE),
(9, '90123456', 'Miguel', 'Ramirez', '1980-02-14', 'M', '555-0109', 'miguel.ramirez@email.com', 'Calle Junin 369, Lima', TRUE),
(10, '01234567', 'Laura', 'Torres', '1993-10-20', 'F', '555-0110', 'laura.torres@email.com', 'Av. Tacna 741, Lima', TRUE),
(11, '11223344', 'Roberto', 'Vargas', '1968-08-03', 'M', '555-0111', 'roberto.vargas@email.com', 'Jr. Ica 852, Lima', TRUE),
(12, '22334455', 'Diana', 'Castro', '1986-11-27', 'F', '555-0112', 'diana.castro@email.com', 'Calle Piura 963, Lima', TRUE),
(13, '33445566', 'Jorge', 'Morales', '1979-05-16', 'M', '555-0113', 'jorge.morales@email.com', 'Av. Cusco 159, Lima', TRUE),
(14, '44556677', 'Gabriela', 'Ortega', '1991-03-09', 'F', '555-0114', 'gabriela.ortega@email.com', 'Jr. Tumbes 357, Lima', TRUE),
(15, '55667788', 'Fernando', 'Herrera', '1984-07-31', 'M', '555-0115', 'fernando.herrera@email.com', 'Calle Trujillo 486, Lima', TRUE),
(16, '66778899', 'Patricia', 'Silva', '1977-01-23', 'F', '555-0116', 'patricia.silva@email.com', 'Av. Chiclayo 753, Lima', TRUE),
(17, '77889900', 'Ricardo', 'Mendoza', '1994-09-05', 'M', '555-0117', 'ricardo.mendoza@email.com', 'Jr. Puno 951, Lima', TRUE),
(18, '88990011', 'Isabel', 'Rojas', '1983-12-11', 'F', '555-0118', 'isabel.rojas@email.com', 'Calle Cajamarca 357, Lima', TRUE),
(19, '99001122', 'Hugo', 'Guerrero', '1976-04-29', 'M', '555-0119', 'hugo.guerrero@email.com', 'Av. Loreto 159, Lima', TRUE),
(20, '00112233', 'Monica', 'Cruz', '1989-08-17', 'F', '555-0120', 'monica.cruz@email.com', 'Jr. Ucayali 753, Lima', TRUE),
(21, '12345001', 'Alejandro', 'Reyes', '1972-02-08', 'M', '555-0121', 'alejandro.reyes@email.com', 'Calle Amazonas 456, Lima', TRUE),
(22, '23456002', 'Valentina', 'Navarro', '1996-06-25', 'F', '555-0122', 'valentina.navarro@email.com', 'Av. Madre de Dios 789, Lima', TRUE),
(23, '34567003', 'Santiago', 'Aguirre', '1981-10-13', 'M', '555-0123', 'santiago.aguirre@email.com', 'Jr. San Martin 321, Lima', TRUE),
(24, '45678004', 'Camila', 'Delgado', '1987-03-04', 'F', '555-0124', 'camila.delgado@email.com', 'Calle Huanuco 654, Lima', TRUE),
(25, '56789005', 'Martin', 'Paredes', '1974-07-19', 'M', '555-0125', 'martin.paredes@email.com', 'Av. Pasco 987, Lima', TRUE),
(26, '67890006', 'Luciana', 'Vega', '1990-11-22', 'F', '555-0126', 'luciana.vega@email.com', 'Jr. Huancavelica 147, Lima', TRUE),
(27, '78901007', 'Emiliano', 'Flores', '1986-01-14', 'M', '555-0127', 'emiliano.flores@email.com', 'Calle Ayacucho 258, Lima', TRUE),
(28, '89012008', 'Mariana', 'Espinoza', '1993-05-28', 'F', '555-0128', 'mariana.espinoza@email.com', 'Av. Apurimac 369, Lima', TRUE),
(29, '90123009', 'Leonardo', 'Soto', '1978-09-10', 'M', '555-0129', 'leonardo.soto@email.com', 'Jr. Huancayo 741, Lima', TRUE),
(30, '01234010', 'Victoria', 'Caceres', '1985-12-02', 'F', '555-0130', 'victoria.caceres@email.com', 'Calle Huacho 852, Lima', TRUE),
(31, '13579001', 'Andres', 'Valenzuela', '1970-04-16', 'M', '555-0131', 'andres.valenzuela@email.com', 'Av. Chimbote 159, Lima', TRUE),
(32, '24680002', 'Daniela', 'Bravo', '1997-08-24', 'F', '555-0132', 'daniela.bravo@email.com', 'Jr. Nazca 357, Lima', TRUE),
(33, '35790003', 'Felipe', 'Araya', '1982-12-07', 'M', '555-0133', 'felipe.araya@email.com', 'Calle Iquitos 486, Lima', TRUE),
(34, '46801004', 'Antonella', 'Pena', '1988-03-21', 'F', '555-0134', 'antonella.pena@email.com', 'Av. Pucallpa 753, Lima', TRUE),
(35, '57912005', 'Maximiliano', 'Carrasco', '1975-06-14', 'M', '555-0135', 'maximiliano.carrasco@email.com', 'Jr. Tarapoto 951, Lima', TRUE),
(36, '68023006', 'Julieta', 'Sandoval', '1992-10-09', 'F', '555-0136', 'julieta.sandoval@email.com', 'Calle Moyobamba 357, Lima', TRUE),
(37, '79134007', 'Agustin', 'Tapia', '1980-02-27', 'M', '555-0137', 'agustin.tapia@email.com', 'Av. Yurimaguas 159, Lima', TRUE),
(38, '80245008', 'Martina', 'Zuniga', '1994-07-03', 'F', '555-0138', 'martina.zuniga@email.com', 'Jr. Jaen 753, Lima', TRUE),
(39, '91356009', 'Benjamin', 'Contreras', '1973-11-18', 'M', '555-0139', 'benjamin.contreras@email.com', 'Calle Bagua 951, Lima', TRUE),
(40, '02467010', 'Emilia', 'Figueroa', '1987-01-06', 'F', '555-0140', 'emilia.figueroa@email.com', 'Av. Bagua Grande 357, Lima', TRUE),
(41, '13578111', 'Damian', 'Sepulveda', '1998-05-11', 'M', '555-0141', 'damian.sepulveda@email.com', 'Jr. Chachapoyas 159, Lima', TRUE),
(42, '24689222', 'Renata', 'Cardenas', '1971-09-29', 'F', '555-0142', 'renata.cardenas@email.com', 'Calle Moyobamba 753, Lima', TRUE),
(43, '35790333', 'Thiago', 'Salazar', '1984-02-02', 'M', '555-0143', 'thiago.salazar@email.com', 'Av. Rioja 951, Lima', TRUE),
(44, '46801444', 'Olivia', 'Maldonado', '1995-06-17', 'F', '555-0144', 'olivia.maldonado@email.com', 'Jr. Lambayeque 357, Lima', TRUE),
(45, '57912555', 'Benicio', 'Escobar', '1977-10-05', 'M', '555-0145', 'benicio.escobar@email.com', 'Calle Ferrenafe 159, Lima', TRUE),
(46, '68023666', 'Alma', 'Palacios', '1991-12-23', 'F', '555-0146', 'alma.palacios@email.com', 'Jr. Chicama 753, Lima', TRUE),
(47, '79134777', 'Bautista', 'Guzman', '1969-08-12', 'M', '555-0147', 'bautista.guzman@email.com', 'Av. Viru 951, Lima', TRUE),
(48, '80245888', 'Celeste', 'Escudero', '1983-04-01', 'F', '555-0148', 'celeste.escudero@email.com', 'Calle Guadalupe 357, Lima', TRUE),
(49, '91356999', 'Ciro', 'Miranda', '1999-12-19', 'M', '555-0149', 'ciro.miranda@email.com', 'Jr. Chepen 159, Lima', TRUE),
(50, '02467100', 'Emma', 'Peralta', '1987-05-20', 'F', '555-0150', 'emma.peralta@email.com', 'Calle Chota 753, Lima', TRUE);

SELECT setval('pacientes_id_seq', 50);

-- =============================================
-- 3. CONTACTOS DE EMERGENCIA
-- =============================================
INSERT INTO contactos_emergencia (paciente_id, nombres_completos, telefono, parentesco) VALUES
(1, 'Maria Martinez', '555-0201', 'Esposa'),
(2, 'Jose Lopez', '555-0202', 'Padre'),
(3, 'Carmen Garcia', '555-0203', 'Esposa'),
(4, 'Roberto Rodriguez', '555-0204', 'Padre'),
(5, 'Diana Sanchez', '555-0205', 'Esposa'),
(6, 'Luis Perez', '555-0206', 'Hermano'),
(7, 'Elena Fernandez', '555-0207', 'Esposa'),
(8, 'Miguel Gonzalez', '555-0208', 'Padre'),
(9, 'Ana Ramirez', '555-0209', 'Esposa'),
(10, 'Juan Torres', '555-0210', 'Padre'),
(11, 'Sofia Vargas', '555-0211', 'Esposa'),
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
-- 4. TRIAJES (40 triajes con IDs 1-40)
-- =============================================
INSERT INTO triajes (id, paciente_id, usuario_id, fecha_hora, motivo_consulta, nivel_urgencia_asignado_ia, nivel_urgencia_final, estado_logistico, notas_medicas, tiempo_atencion_segundos, activo) VALUES
(1, 1, 2, NOW() - INTERVAL '2 hours', 'Dolor de pecho intenso', 'RED', 'RED', 'Atendido', 'Paciente con sintomas de infarto. Atencion inmediata.', 480, TRUE),
(2, 2, 3, NOW() - INTERVAL '3 hours', 'Fiebre alta y dolor de cabeza', 'YELLOW', 'YELLOW', 'Atendido', 'Fiebre 39C. Administrado antipiretico.', 900, TRUE),
(3, 3, 2, NOW() - INTERVAL '4 hours', 'Dolor abdominal agudo', 'ORANGE', 'RED', 'Atendido', 'Apendicitis aguda. Derivado a cirugia.', 1200, TRUE),
(4, 4, 4, NOW() - INTERVAL '5 hours', 'Tos y congestion nasal', 'GREEN', 'GREEN', 'Atendido', 'Resfriado comun. Reposo indicado.', 600, TRUE),
(5, 5, 3, NOW() - INTERVAL '6 hours', 'Fractura de brazo', 'YELLOW', 'YELLOW', 'Atendido', 'Fractura de cubito. Yesado aplicado.', 1800, TRUE),
(6, 6, 2, NOW() - INTERVAL '1 hour', 'Migrana severa', 'GREEN', 'YELLOW', 'En Atencion', 'Dolor craneal intenso. Analgesico administrado.', 720, TRUE),
(7, 7, 4, NOW() - INTERVAL '30 minutes', 'Quemadura de segundo grado', 'YELLOW', 'YELLOW', 'En Atencion', 'Quemadura en antebrazo. Curacion en proceso.', 900, TRUE),
(8, 8, 3, NOW() - INTERVAL '45 minutes', 'Dificultad respiratoria', 'RED', 'RED', 'Llamado', 'Posible asma severo. Oxigenoterapia iniciada.', NULL, TRUE),
(9, 9, 2, NOW() - INTERVAL '10 minutes', 'Corte en mano', 'BLUE', 'GREEN', 'En Espera', 'Laceracion superficial. Esperando curacion.', NULL, TRUE),
(10, 10, 4, NOW() - INTERVAL '15 minutes', 'Nauseas y vomitos', 'GREEN', 'GREEN', 'En Espera', 'Gastroenteritis probable. Hidratacion oral.', NULL, TRUE),

-- Febrero 2024
(11, 11, 2, '2024-02-15 14:30:00', 'Dolor toracico', 'RED', 'RED', 'Atendido', 'Infarto agudo al miocardio. Trombolisis aplicada.', 420, TRUE),
(12, 12, 3, '2024-02-14 09:15:00', 'Dolor de garganta', 'GREEN', 'GREEN', 'Atendido', 'Faringitis estreptococica. Antibiotico prescrito.', 540, TRUE),
(13, 13, 4, '2024-02-13 16:45:00', 'Trauma craneoencefalico', 'RED', 'RED', 'Atendido', 'Accidente de transito. TAC realizado.', 1800, TRUE),
(14, 14, 2, '2024-02-12 11:20:00', 'Dolor lumbar', 'YELLOW', 'GREEN', 'Atendido', 'Lumbalgia aguda. AINEs indicados.', 780, TRUE),
(15, 15, 3, '2024-02-11 08:00:00', 'Hemorragia nasal', 'ORANGE', 'YELLOW', 'Atendido', 'Epistaxis. Tamponado anterior realizado.', 660, TRUE),
(16, 16, 4, '2024-02-10 19:30:00', 'Alergia alimentaria', 'YELLOW', 'YELLOW', 'Atendido', 'Shock anafilactico. Adrenalina administrada.', 480, TRUE),
(17, 17, 2, '2024-02-09 13:45:00', 'Dolor de oido', 'BLUE', 'GREEN', 'Atendido', 'Otitis media. Antibiotico topico indicado.', 600, TRUE),
(18, 18, 3, '2024-02-08 10:00:00', 'Convulsiones', 'RED', 'RED', 'Atendido', 'Crisis epileptica. Diazepam IV administrado.', 900, TRUE),
(19, 19, 4, '2024-02-07 15:20:00', 'Dolor articular', 'GREEN', 'GREEN', 'Atendido', 'Artritis reumatoide. AINEs indicados.', 720, TRUE),
(20, 20, 2, '2024-02-06 07:45:00', 'Hemoptisis', 'ORANGE', 'ORANGE', 'Atendido', 'Tuberculosis sospechada. Aislamiento indicado.', 1200, TRUE),

-- Enero 2024
(21, 21, 3, '2024-01-25 12:00:00', 'Sincope', 'ORANGE', 'ORANGE', 'Atendido', 'Perdida de conciencia breve. Estudio cardiologico.', 840, TRUE),
(22, 22, 2, '2024-01-24 18:30:00', 'Herida de bala', 'RED', 'RED', 'Atendido', 'Trauma penetrante. Cirugia de emergencia.', 3600, TRUE),
(23, 23, 4, '2024-01-23 09:00:00', 'Infeccion urinaria', 'YELLOW', 'YELLOW', 'Atendido', 'Cistitis. Antibiotico oral prescrito.', 540, TRUE),
(24, 24, 3, '2024-01-22 14:15:00', 'Dolor ocular', 'YELLOW', 'YELLOW', 'Atendido', 'Uveitis. Derivar a oftalmologia.', 660, TRUE),
(25, 25, 2, '2024-01-21 11:00:00', 'Palpitaciones', 'YELLOW', 'ORANGE', 'Atendido', 'Arritmia supraventricular. ECG anormal.', 780, TRUE),
(26, 26, 4, '2024-01-20 16:45:00', 'Esguince de tobillo', 'GREEN', 'GREEN', 'Atendido', 'Trauma leve. Vendaje compresivo.', 600, TRUE),
(27, 27, 3, '2024-01-19 08:30:00', 'Dolor abdominal difuso', 'YELLOW', 'YELLOW', 'Atendido', 'Gastroenteritis. Hidratacion IV.', 900, TRUE),
(28, 28, 2, '2024-01-18 20:00:00', 'Cefalea explosiva', 'RED', 'RED', 'Atendido', 'Hemorragia subaracnoidea. TAC urgente.', 1500, TRUE),
(29, 29, 4, '2024-01-17 10:30:00', 'Erupcion cutanea', 'GREEN', 'GREEN', 'Atendido', 'Dermatitis alergica. Antihistaminico.', 480, TRUE),
(30, 30, 3, '2024-01-16 13:00:00', 'Dolor toracico pleuritico', 'ORANGE', 'ORANGE', 'Atendido', 'Neumotorax. Drenaje toracico.', 2100, TRUE),

-- Diciembre 2023
(31, 31, 2, '2023-12-28 15:30:00', 'Intoxicacion alimentaria', 'GREEN', 'GREEN', 'Atendido', 'Vomitos y diarrea. Hidratacion.', 720, TRUE),
(32, 32, 3, '2023-12-27 09:45:00', 'Dolor de espalda', 'BLUE', 'GREEN', 'Atendido', 'Contractura muscular. Fisioterapia indicada.', 540, TRUE),
(33, 33, 4, '2023-12-26 11:20:00', 'Cuerpo extrano en ojo', 'YELLOW', 'YELLOW', 'Atendido', 'Extraccion de cuerpo extrano. Antibiotico.', 480, TRUE),
(34, 34, 2, '2023-12-25 19:00:00', 'Quemadura electrica', 'RED', 'RED', 'Atendido', 'Electrocucion. Monitorizacion cardiaca.', 1800, TRUE),
(35, 35, 3, '2023-12-24 14:00:00', 'Bronquitis aguda', 'YELLOW', 'YELLOW', 'Atendido', 'Broncoespasmo. Broncodilatadores.', 840, TRUE),
(36, 36, 4, '2023-12-23 10:15:00', 'Dolor dental', 'BLUE', 'BLUE', 'Atendido', 'Absceso dental. Antibiotico + analgesico.', 360, TRUE),
(37, 37, 2, '2023-12-22 17:30:00', 'Hipotermia', 'ORANGE', 'ORANGE', 'Atendido', 'Exposicion al frio. Reanimacion.', 1200, TRUE),
(38, 38, 3, '2023-12-21 08:00:00', 'Calculo renal', 'YELLOW', 'YELLOW', 'Atendido', 'Colico nefritico. AINEs + espasmoliticos.', 1800, TRUE),
(39, 39, 4, '2023-12-20 13:45:00', 'Insomnio cronico', 'BLUE', 'BLUE', 'Atendido', 'Trastorno del sueno. Derivado a psiquiatria.', 420, TRUE),
(40, 40, 2, '2023-12-19 16:00:00', 'Amputacion parcial', 'RED', 'RED', 'Atendido', 'Trauma laboral. Reimplante no viable.', 2400, TRUE);

SELECT setval('triajes_id_seq', 40);

-- =============================================
-- 5. SIGNOS VITALES (solo para triajes 1-40)
-- =============================================
INSERT INTO signos_vitales (triaje_id, presion_sistolica, presion_diastolica, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, saturacion_o2, nota_suplementaria) VALUES
(1, 180, 110, 110, 24, 37.2, 95, 'Hipertension severa'),
(2, 130, 85, 95, 20, 39.1, 98, 'Fiebre alta'),
(3, 140, 90, 105, 22, 38.0, 97, 'Dolor abdominal'),
(4, 120, 80, 75, 18, 37.0, 99, 'Estable'),
(5, 125, 82, 88, 19, 36.8, 100, 'Dolor moderado'),
(6, 118, 78, 72, 16, 36.5, 99, 'Dolor craneal'),
(7, 128, 84, 92, 20, 37.1, 98, 'Quemadura'),
(8, 110, 75, 115, 28, 37.0, 88, 'Dificultad respiratoria'),
(9, 122, 80, 70, 18, 36.7, 100, 'Lesion leve'),
(10, 124, 82, 78, 19, 37.2, 99, 'Deshidratacion leve'),
(11, 160, 100, 105, 22, 37.0, 94, 'Infarto'),
(12, 118, 76, 82, 18, 37.5, 99, 'Faringitis'),
(13, 90, 60, 120, 25, 36.0, 92, 'Trauma craneal'),
(14, 128, 82, 78, 18, 36.8, 98, 'Dolor lumbar'),
(15, 135, 88, 95, 20, 37.0, 97, 'Epistaxis'),
(16, 85, 55, 115, 24, 36.5, 93, 'Anafilaxia'),
(17, 120, 78, 72, 18, 37.2, 99, 'Otitis'),
(18, 140, 90, 125, 22, 38.5, 96, 'Convulsiones'),
(19, 132, 86, 80, 19, 36.9, 98, 'Artritis'),
(20, 145, 92, 100, 24, 37.8, 95, 'Hemoptisis'),
(21, 110, 70, 95, 20, 36.5, 97, 'Sincope'),
(22, 80, 50, 130, 30, 35.0, 85, 'Shock hemorragico'),
(23, 125, 80, 88, 19, 37.6, 99, 'Infeccion urinaria'),
(24, 120, 78, 76, 18, 36.8, 100, 'Dolor ocular'),
(25, 138, 88, 110, 22, 37.1, 97, 'Arritmia'),
(26, 122, 80, 70, 18, 36.5, 100, 'Trauma leve'),
(27, 118, 76, 85, 20, 37.4, 98, 'Gastroenteritis'),
(28, 175, 105, 115, 24, 37.0, 94, 'Hemorragia cerebral'),
(29, 120, 78, 74, 18, 37.0, 99, 'Alergia'),
(30, 140, 90, 105, 26, 37.2, 91, 'Neumotorax'),
(31, 110, 72, 88, 20, 37.8, 98, 'Intoxicacion'),
(32, 115, 75, 70, 16, 36.5, 99, 'Contractura'),
(33, 125, 82, 78, 18, 37.0, 100, 'Trauma ocular'),
(34, 135, 88, 125, 28, 36.0, 90, 'Electrocucion'),
(35, 118, 78, 95, 24, 37.5, 96, 'Bronquitis'),
(36, 120, 80, 72, 18, 37.0, 99, 'Dolor dental'),
(37, 95, 60, 55, 12, 33.0, 92, 'Hipotermia'),
(38, 128, 85, 100, 22, 38.0, 97, 'Calculo renal'),
(39, 122, 78, 68, 16, 36.5, 99, 'Insomnio'),
(40, 70, 45, 140, 32, 35.5, 88, 'Shock traumatico');

-- =============================================
-- 6. SINTOMAS DE TRIAJE
-- =============================================
INSERT INTO sintomas_triaje (triaje_id, sintoma, intensidad, descripcion_libre) VALUES
(1, 'Dolor toracico', 'Grave', 'Oprimido, irradia a brazo izquierdo'),
(1, 'Sudoracion', 'Moderado', 'Sudoracion profusa'),
(1, 'Nauseas', 'Leve', NULL),
(2, 'Fiebre', 'Moderado', '39C desde hace 2 dias'),
(2, 'Dolor de cabeza', 'Moderado', 'Frontal y constante'),
(2, 'Malestar general', 'Moderado', NULL),
(3, 'Dolor abdominal', 'Grave', 'Fosa iliaca derecha'),
(3, 'Vomitos', 'Moderado', 'Alimentarios'),
(3, 'Fiebre', 'Leve', '37.8C'),
(4, 'Tos', 'Leve', 'Productiva'),
(4, 'Congestion nasal', 'Leve', NULL),
(5, 'Dolor', 'Grave', 'Intenso en antebrazo'),
(5, 'Deformidad', 'Moderado', 'Angulacion visible'),
(6, 'Dolor de cabeza', 'Grave', 'Pulsatil unilateral'),
(6, 'Fotofobia', 'Moderado', 'Intolerancia a la luz'),
(8, 'Disnea', 'Grave', 'Dificultad para respirar'),
(8, 'Sibilancias', 'Moderado', 'Al espirar'),
(11, 'Dolor toracico', 'Grave', 'Tipo opresivo'),
(13, 'Alteracion conciencia', 'Grave', 'Glasgow 12'),
(13, 'Dolor de cabeza', 'Grave', 'Intenso'),
(14, 'Dolor lumbar', 'Moderado', 'Irradia a gluteo'),
(18, 'Convulsiones', 'Grave', 'Tonico-clonicas generalizadas'),
(22, 'Dolor', 'Grave', 'Herida de bala en abdomen'),
(22, 'Hemorragia', 'Grave', 'Activa'),
(28, 'Cefalea explosiva', 'Grave', 'Peor dolor de su vida'),
(28, 'Rigidez de nuca', 'Grave', NULL),
(30, 'Dolor toracico', 'Grave', 'Pleuritico'),
(30, 'Disnea', 'Grave', 'Repentina'),
(34, 'Quemadura', 'Grave', 'Entrada y salida'),
(40, 'Amputacion', 'Grave', 'Dedos de mano derecha'),
(28, 'Deficit motor', 'Moderado', 'Debilidad en brazo izquierdo'),
(30, 'Afasia', 'Leve', 'Dificultad para hablar'),
(38, 'Vomito', 'Moderado', 'Nauseas persistentes');

-- =============================================
-- 7. RESULTADOS IA
-- =============================================
INSERT INTO resultados_ia (triaje_id, prompt_enviado, respuesta_raw_llm, diagnosticos_json, recomendaciones_json, modelo_utilizado, latencia_segundos) VALUES
(1, 'Prompt: Paciente masculino 38 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "Sindrome coronario agudo", "probabilidad": 0.85}]'::jsonb, '[{"accion": "ECG 12 derivaciones", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.5),
(3, 'Prompt: Paciente masculino 45 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "Apendicitis aguda", "probabilidad": 0.80}]'::jsonb, '[{"accion": "Cirugia de emergencia", "prioridad": "urgente"}]'::jsonb, 'gpt-4', 2.2),
(11, 'Prompt: Paciente masculino 55 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "IAM", "probabilidad": 0.90}]'::jsonb, '[{"accion": "Trombolisis", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.1),
(13, 'Prompt: Paciente masculino 45 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "TCE severo", "probabilidad": 0.88}]'::jsonb, '[{"accion": "TAC craneo", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.8),
(18, 'Prompt: Paciente masculino 44 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "Crisis epileptica", "probabilidad": 0.92}]'::jsonb, '[{"accion": "Diazepam 10mg IV", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 1.9),
(22, 'Prompt: Paciente masculino 46 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "Trauma penetrante", "probabilidad": 0.95}]'::jsonb, '[{"accion": "Laparotomia", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.3),
(28, 'Prompt: Paciente femenina 31 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "HSA", "probabilidad": 0.87}]'::jsonb, '[{"accion": "TAC urgente", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.0),
(40, 'Prompt: Paciente femenina 37 años...', 'RESPONSE: Nivel RED', '[{"diagnostico": "ACV isquemico", "probabilidad": 0.91}]'::jsonb, '[{"accion": "Trombolisis IV", "prioridad": "inmediata"}]'::jsonb, 'gpt-4', 2.4);

-- =============================================
-- 8. HCE ANTECEDENTES
-- =============================================
INSERT INTO hce_antecedentes (paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo) VALUES
(1, 'Patologia', 'Hipertension arterial', 'HTA diagnosticada hace 5 años', '2019-03-15', TRUE),
(1, 'Medicamento', 'Losartan', '50mg diario', '2019-03-15', TRUE),
(1, 'Alergia', 'Penicilina', 'Urticaria', '2010-06-20', TRUE),
(3, 'Patologia', 'Diabetes mellitus tipo 2', 'DM2 diagnosticada 2020', '2020-11-10', TRUE),
(3, 'Medicamento', 'Metformina', '850mg cada 12 horas', '2020-11-10', TRUE),
(5, 'Patologia', 'Asma', 'Asma moderada persistente', '2015-08-05', TRUE),
(5, 'Medicamento', 'Salbutamol', 'Inhalador de rescate', '2015-08-05', TRUE),
(8, 'Patologia', 'Epilepsia', 'Desde adolescencia', '2008-03-12', TRUE),
(11, 'Patologia', 'Dislipidemia', 'Colesterol elevado', '2018-01-20', TRUE),
(13, 'Cirugia', 'Apendicectomia', 'Cirugia laparoscopica', '2015-07-10', FALSE),
(17, 'Alergia', 'Yodo', 'Reaccion cutanea', '2012-09-15', TRUE),
(19, 'Patologia', 'Artritis reumatoide', 'Diagnosticada 2019', '2019-04-22', TRUE),
(25, 'Patologia', 'Arritmia', 'FA paroxistica', '2020-02-14', TRUE),
(28, 'Alergia', 'Latex', 'Anafilaxia leve', '2015-12-03', TRUE),
(31, 'Patologia', 'EPOC', 'Enfermedad pulmonar cronica', '2017-11-18', TRUE),
(35, 'Patologia', 'Bronquitis cronica', 'Fumador ex 20 paquetes-año', '2016-09-25', TRUE),
(38, 'Cirugia', 'Colecistectomia', 'Por colelitiasis', '2010-05-15', FALSE);

-- =============================================
-- 9. HCE CONSULTAS PREVIAS
-- =============================================
INSERT INTO hce_consulta_previa (paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento) VALUES
(1, '2023-08-15 09:00:00', 'Control de hipertension', 'HTA compensada', 'Continuar Losartan 50mg'),
(3, '2023-06-20 14:00:00', 'Control DM2', 'DM2 compensada HbA1c 7.2%', 'Continuar Metformina'),
(5, '2023-09-12 11:00:00', 'Exacerbacion asmatica', 'Asma moderada', 'Prednisona 5 dias'),
(8, '2023-07-25 16:00:00', 'Control epilepsia', 'Epilepsia estable', 'Continuar valproato'),
(11, '2023-10-08 10:00:00', 'Control dislipidemia', 'Dislipidemia mejorada', 'Continuar estatina'),
(19, '2023-05-18 09:15:00', 'Control artritis', 'AR actividad moderada', 'Ajustar MTX'),
(25, '2023-08-22 14:30:00', 'Palpitaciones', 'FA paroxistica', 'Anticoagulante iniciado'),
(31, '2023-09-30 11:45:00', 'Exacerbacion EPOC', 'EPOC exacerbada', 'Corticoides + antibiotico'),
(38, '2023-04-12 10:30:00', 'Colico nefritico', 'Calculo renal', 'Analgesicos + hidratacion'),
(40, '2023-07-08 09:00:00', 'Control ACV', 'Secuelas leves', 'Rehabilitacion');

-- =============================================
-- 10. LOGS AUDITORIA
-- =============================================
INSERT INTO logs_auditoria (usuario_id, accion, modulo, registro_id, datos_anteriores, datos_nuevos, ip_address, user_agent, timestamp) VALUES
(2, 'INSERT', 'triajes', 1, NULL, '{"paciente_id": 1, "nivel": "RED"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0', NOW() - INTERVAL '2 hours'),
(2, 'UPDATE', 'triajes', 1, '{"estado": "En Espera"}'::jsonb, '{"estado": "En Atencion"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0', NOW() - INTERVAL '1 hour 30 minutes'),
(2, 'UPDATE', 'triajes', 1, '{"estado": "En Atencion"}'::jsonb, '{"estado": "Atendido"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0', NOW() - INTERVAL '30 minutes'),
(3, 'INSERT', 'triajes', 2, NULL, '{"paciente_id": 2, "nivel": "YELLOW"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0', NOW() - INTERVAL '3 hours'),
(3, 'UPDATE', 'triajes', 2, '{"nivel_ia": "RED", "nivel_final": null}'::jsonb, '{"nivel_ia": "RED", "nivel_final": "YELLOW"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0', NOW() - INTERVAL '2 hours 30 minutes'),
(4, 'INSERT', 'triajes', 4, NULL, '{"paciente_id": 4, "nivel": "GREEN"}'::jsonb, '192.168.1.12'::inet, 'Mozilla/5.0', NOW() - INTERVAL '5 hours'),
(4, 'INSERT', 'signos_vitales', 4, NULL, '{"triaje_id": 4, "fc": 75}'::jsonb, '192.168.1.12'::inet, 'Mozilla/5.0', NOW() - INTERVAL '4 hours 45 minutes'),
(2, 'STATUS_CHANGE', 'triajes', 8, '{"estado": "En Espera"}'::jsonb, '{"estado": "Llamado"}'::jsonb, '192.168.1.10'::inet, 'Mozilla/5.0', NOW() - INTERVAL '20 minutes'),
(3, 'STATUS_CHANGE', 'triajes', 8, '{"estado": "Llamado"}'::jsonb, '{"estado": "En Atencion"}'::jsonb, '192.168.1.11'::inet, 'Mozilla/5.0', NOW() - INTERVAL '5 minutes'),
(3, 'INSERT', 'triajes', 8, NULL, '{"paciente_id": 8, "nivel": "RED"}'::jsonb, '192.168.1.20'::inet, 'Mozilla/5.0', NOW() - INTERVAL '45 minutes'),
(2, 'INSERT', 'triajes', 9, NULL, '{"paciente_id": 9, "nivel": "GREEN"}'::jsonb, '192.168.1.21'::inet, 'Mozilla/5.0', NOW() - INTERVAL '10 minutes'),
(1, 'INSERT', 'triajes', 40, NULL, '{"paciente_id": 40, "nivel": "RED"}'::jsonb, '192.168.1.50'::inet, 'PostmanRuntime/7.36.0', '2023-12-19 16:00:00'),
(7, 'INSERT', 'triajes', 11, NULL, '{"paciente_id": 11, "nivel": "RED"}'::jsonb, '192.168.1.17'::inet, 'Mozilla/5.0', '2024-02-15 14:30:00'),
(7, 'UPDATE', 'triajes', 11, '{"estado": "En Espera"}'::jsonb, '{"estado": "Atendido"}'::jsonb, '192.168.1.17'::inet, 'Mozilla/5.0', '2024-02-15 15:30:00');

-- =============================================
-- FIN
-- =============================================
