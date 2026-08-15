import sqlite3
import logging
from werkzeug.security import generate_password_hash
from database import get_connection

# Configuramos la terminal para ver los mensajes de éxito
logging.basicConfig(level=logging.INFO, format='%(message)s')

def insert_seed_data():
    """
    Inyecta datos iniciales en la base de datos para pruebas locales.
    Verifica primero si los datos ya existen para evitar duplicados.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Crear el SuperUsuario
        # Primero revisamos si ya existe para no duplicarlo
        cursor.execute("SELECT id FROM usuarios WHERE username = 'admin'")
        if not cursor.fetchone():
            # Encriptamos la contraseña 'admin123'
            password_encriptada = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO usuarios (username, password_hashed, rol)
                VALUES (?, ?, ?)
            ''', ('admin', password_encriptada, 'SuperUsuario'))
            logging.info("👤 SuperUsuario creado: Usuario -> 'admin' | Clave -> 'admin123'")

        # 2. Cargar Clientes de prueba
        cursor.execute("SELECT count(*) FROM clientes")
        if cursor.fetchone()[0] == 0:
            clientes = [
                ("Kariannys", "V-27123456", "", "0414-1234567", "", "Centro", "Calle Monagas, Casa 12", "Cerca de la plaza", "Frecuente"),
                ("Carlos Mendoza", "V-15987654", "", "0424-7654321", "", "Urb. Villa de los Ángeles", "Manzana 3, Casa 45", "Portón negro", "Nuevo")
            ]
            cursor.executemany('''
                INSERT INTO clientes (nombre, cedula, foto_cedula_path, telefono_1, telefono_2, sector, direccion, referencia, clasificacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', clientes)
            logging.info("👥 Clientes de prueba insertados.")

        # 3. Cargar Lavadoras de prueba
        cursor.execute("SELECT count(*) FROM lavadoras")
        if cursor.fetchone()[0] == 0:
            lavadoras = [
                ("LG", 12.0, 1, "Disponible"), # 1 = Tiene bomba de agua
                ("Samsung", 10.0, 1, "Disponible"),
                ("Mabe", 14.0, 0, "Mantenimiento") # 0 = No tiene bomba de agua
            ]
            cursor.executemany('''
                INSERT INTO lavadoras (marca, capacidad_kg, bomba, estatus)
                VALUES (?, ?, ?, ?)
            ''', lavadoras)
            logging.info("🧼 Lavadoras de prueba insertadas.")

        # 4. Cargar Choferes de prueba
        cursor.execute("SELECT count(*) FROM choferes")
        if cursor.fetchone()[0] == 0:
            choferes = [
                ("Willmer", "0412-5556677", "Chevrolet LUV D-Max", "A12B34C", "Activo"),
                ("Luis Perez", "0414-9998877", "Ford F-150", "X98Y76Z", "Activo")
            ]
            cursor.executemany('''
                INSERT INTO choferes (nombre, telefono, vehiculo, placa, estatus)
                VALUES (?, ?, ?, ?, ?)
            ''', choferes)
            logging.info("🚚 Choferes de prueba insertados.")

        conn.commit()
        logging.info("✅ Carga de datos semilla finalizada con éxito.")

if __name__ == "__main__":
    print("Iniciando inyección de datos semilla...")
    insert_seed_data()