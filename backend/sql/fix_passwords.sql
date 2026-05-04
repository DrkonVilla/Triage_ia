-- Actualizar contraseñas a 'password123' (hash bcrypt válido)
-- Generado con: bcrypt.hashpw(b'password123', bcrypt.gensalt(rounds=12))

UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id = 1;  -- gerente1
UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id = 2;  -- enfermera1
UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id = 3;  -- enfermera2
UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id = 4;  -- medico1
UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id = 5;  -- auditor1
UPDATE usuarios SET hashed_password = '$2b$12$4l.zO17jBtqOxC3CXqBO5OQsj6K6gF5XuIK3ZTz5V2VZ9Q.gq2.CO' WHERE id IN (6,7,8,9,10,11,12);  -- resto

-- Verificar
SELECT username, rol, activo FROM usuarios;
