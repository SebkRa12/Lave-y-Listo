import json
import logging
from database import get_connection

# Configuramos un logger de consola para ver en la terminal si algo falla
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def log_audit(usuario_id: int, accion: str, modulo: str, detalles: dict) -> bool:
    """
    Función interceptora de seguridad. 
    Guarda automáticamente un registro inmutable de cada acción crítica.
    
    :param usuario_id: ID del usuario que ejecuta la acción (SuperUsuario, Admin, Chofer).
    :param accion: Debe ser 'CREAR', 'EDITAR', 'ELIMINAR', 'LOGIN' o 'LOGOUT'.
    :param modulo: Tabla o sección afectada (ej: 'CLIENTES', 'LAVADORAS', 'SERVICIOS').
    :param detalles: Diccionario en Python con los datos o los cambios realizados.
    :return: True si se guardó con éxito, False si hubo un error.
    """
    acciones_permitidas = ['CREAR', 'EDITAR', 'ELIMINAR', 'LOGIN', 'LOGOUT']
    accion = accion.upper()

    if accion not in acciones_permitidas:
        logging.error(f"Intento de auditoría con acción no permitida: {accion}")
        return False

    # Convertimos el diccionario a una cadena JSON de forma segura
    try:
        detalles_json = json.dumps(detalles, ensure_ascii=False)
    except TypeError as e:
        logging.error(f"Error al convertir detalles a JSON: {e}")
        detalles_json = '{"error": "datos_no_serializables"}'

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO auditoria_logs (usuario_id, accion, modulo, detalles_json)
                VALUES (?, ?, ?, ?)
            ''', (usuario_id, accion, modulo, detalles_json))
            conn.commit()
            
            logging.info(f"🛡️ Auditoría: {accion} en módulo {modulo} por Usuario {usuario_id}")
            return True
            
    except Exception as e:
        # Si falla el registro de auditoría, queremos saberlo, pero sin tumbar la aplicación
        logging.error(f"Error crítico guardando log de auditoría: {e}")
        return False

# --- Pequeño test para verificar que funcione ---
if __name__ == "__main__":
    print("Probando el motor de auditoría...")
    # Simulamos que el usuario 1 editó el estatus de la lavadora 5
    exito = log_audit(
        usuario_id=1, 
        accion="EDITAR", 
        modulo="LAVADORAS", 
        detalles={"lavadora_id": 5, "estatus_anterior": "Disponible", "estatus_nuevo": "Mantenimiento"}
    )
    if exito:
        print("✅ Motor de auditoría funcionando y guardando en base de datos.")