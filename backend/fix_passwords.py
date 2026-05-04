"""
Script para actualizar contraseñas de usuarios a 'password123'
"""
import asyncio
import bcrypt
import asyncpg

async def fix_passwords():
    # Generar hash bcrypt para 'password123'
    password = b"password123"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
    hashed_str = hashed.decode('utf-8')
    print(f"Hash generado: {hashed_str}")
    
    # Conectar a la base de datos
    conn = await asyncpg.connect("postgresql://postgres:123@localhost:5432/triaje_db")
    
    try:
        # Actualizar todos los usuarios
        result = await conn.execute(
            "UPDATE usuarios SET hashed_password = $1 WHERE id IN (1,2,3,4,5,6,7,8,9,10,11,12)",
            hashed_str
        )
        print(f"✅ Contraseñas actualizadas")
        
        # Verificar
        usuarios = await conn.fetch("SELECT id, username, rol, activo FROM usuarios ORDER BY id")
        print("\n📋 Usuarios en la base de datos:")
        for u in usuarios:
            print(f"  ID {u['id']}: {u['username']} (rol: {u['rol']}, activo: {u['activo']})")
        
        print("\n✅ Listo! Ahora puedes iniciar sesión con cualquier usuario usando 'password123'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(fix_passwords())
