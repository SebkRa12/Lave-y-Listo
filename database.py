import os
import sqlite3

DB_NAME = "lave_y_listo.db"

def get_connection():
    """Crea y retorna una conexión a la base de datos con llaves foráneas activas."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Inicializa el esquema de la base de datos limpiando y creando las tablas."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Limpieza total en orden inverso
        cursor.execute('DROP TABLE IF EXISTS auditoria_logs')
        cursor.execute('DROP TABLE IF EXISTS servicios')
        cursor.execute('DROP TABLE IF EXISTS choferes')
        cursor.execute('DROP TABLE IF EXISTS lavadoras')
        cursor.execute('DROP TABLE IF EXISTS clientes')
        cursor.execute('DROP TABLE IF EXISTS usuarios')

        # 1. Tabla Usuarios
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hashed TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('SuperUsuario', 'Admin', 'Chofer'))
            )
        ''')

        # 2. Tabla Clientes
        cursor.execute('''
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cedula TEXT UNIQUE NOT NULL,
                foto_cedula_path TEXT,
                telefono_1 TEXT NOT NULL,
                telefono_2 TEXT,
                sector TEXT NOT NULL,
                direccion TEXT NOT NULL,
                referencia TEXT,
                clasificacion TEXT DEFAULT 'Nuevo' CHECK(clasificacion IN ('Nuevo', 'Frecuente', 'VIP', 'Lista Negra'))
            )
        ''')

        # 3. Tabla Lavadoras
        cursor.execute('''
            CREATE TABLE lavadoras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT NOT NULL,
                capacidad_kg REAL NOT NULL,
                bomba BOOLEAN NOT NULL CHECK (bomba IN (0, 1)),
                estatus TEXT DEFAULT 'Disponible' CHECK(estatus IN ('Disponible', 'Alquilada', 'Mantenimiento')),
                contador_servicios INTEGER DEFAULT 0,
                historico_mantenimiento TEXT
            )
        ''')

        # 4. Tabla Choferes
        cursor.execute('''
            CREATE TABLE choferes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                vehiculo TEXT,
                placa TEXT,
                estatus TEXT DEFAULT 'Activo' CHECK(estatus IN ('Activo', 'Inactivo'))
            )
        ''')

        # 5. Tabla Servicios
        cursor.execute('''
            CREATE TABLE servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                cliente_id INTEGER NOT NULL,
                lavadora_id INTEGER NOT NULL,
                chofer_id INTEGER NOT NULL,
                turno TEXT NOT NULL,
                hora_inicio DATETIME,
                hora_fin_estimada DATETIME,
                estatus TEXT DEFAULT 'Agendado' CHECK(estatus IN ('Agendado', 'En Curso', 'Por Retirar', 'Finalizado', 'Cancelado')),
                monto_usd REAL NOT NULL,
                metodo_pago TEXT CHECK(metodo_pago IN ('Efectivo', 'Pago Movil', 'Transferencia', 'Pendiente')),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE RESTRICT,
                FOREIGN KEY (lavadora_id) REFERENCES lavadoras (id) ON DELETE RESTRICT,
                FOREIGN KEY (chofer_id) REFERENCES choferes (id) ON DELETE RESTRICT
            )
        ''')

        # 6. Tabla Auditoria Logs
        cursor.execute('''
            CREATE TABLE auditoria_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER,
                accion TEXT NOT NULL CHECK(accion IN ('CREAR', 'EDITAR', 'ELIMINAR', 'LOGIN', 'LOGOUT')),
                modulo TEXT NOT NULL,
                detalles_json TEXT NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
            )
        ''')

        conn.commit()
        print("✅ Base de datos 'lave_y_listo.db' creada/verificada correctamente.")

if __name__ == "__main__":
    init_db()