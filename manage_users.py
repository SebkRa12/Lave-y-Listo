import sqlite3
from werkzeug.security import generate_password_hash

def crear_tabla():
    """Crea la tabla usuarios si no existe para evitar errores"""
    conn = sqlite3.connect('lave_y_listo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def agregar_usuario(username, password_plana, role):
    crear_tabla()  # Asegura que la tabla exista antes de insertar
    conn = sqlite3.connect('lave_y_listo.db')
    cursor = conn.cursor()
    
    hashed_password = generate_password_hash(password_plana)
    
    try:
        cursor.execute('''
            INSERT INTO usuarios (username, password, role)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, role))
        conn.commit()
        print(f"¡Usuario '{username}' con rol '{role}' creado exitosamente!")
    except sqlite3.IntegrityError:
        print(f"Error: El usuario '{username}' ya existe en la base de datos.")
    finally:
        conn.close()

if __name__ == "__main__":
    # Agrega a tus usuarios aquí:
    agregar_usuario("veronica", "12345678", "Chofer")
    agregar_usuario("admin", "admin123", "Administrador")
    
    print("¡Proceso de usuarios finalizado!")