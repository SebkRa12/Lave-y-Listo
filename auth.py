from werkzeug.security import check_password_hash
from database import get_connection

def authenticate_user(username, password):
    """
    Verifica las credenciales del usuario contra la base de datos.
    Retorna un diccionario con los datos del usuario si es exitoso, o None si falla.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hashed, rol FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()

        # Validamos que el usuario exista y que la contraseña coincida
        if user and check_password_hash(user['password_hashed'], password):
            return {
                "id": user['id'],
                "username": user['username'],
                "rol": user['rol']
            }
            
    return None