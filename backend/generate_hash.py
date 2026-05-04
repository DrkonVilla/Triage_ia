import bcrypt

password = b"password123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(f"Hash para 'password123': {hashed.decode()}")

# Verificar que funciona
result = bcrypt.checkpw(password, hashed)
print(f"Verificación: {result}")
