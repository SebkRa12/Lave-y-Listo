import sqlite3
from werkzeug.security import check_password_hash

def authenticate_user(username, password):
    conn = sqlite3.connect('lave_y_listo.db')
    cursor = conn.cursor()
    # Usamos 'password' y 'role' que son los nombres correctos de las columnas
    cursor.execute('SELECT id, username, password, role FROM usuarios WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        user_id, db_username, stored_password, role = result
        if check_password_hash(stored_password, password):
            # Devolvemos un diccionario con los datos que app.py necesita
            return {"id": user_id, "username": db_username, "role": role}
            
    return None