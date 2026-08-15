import streamlit as st
from auth import authenticate_user

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Lave y Listo", page_icon="🧼", layout="wide")

# --- INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'rol' not in st.session_state:
    st.session_state['rol'] = ""

def login():
    """Muestra el formulario de inicio de sesión."""
    st.title("🔐 Acceso al Sistema - Lave y Listo")
    st.write("Por favor, ingresa tus credenciales.")
    
    # Usamos st.form para agrupar los inputs y evitar recargas por cada letra
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")

        if submit:
            user_data = authenticate_user(usuario, clave)
            if user_data:
                # Guardamos los datos en la sesión
                st.session_state['logged_in'] = True
                st.session_state['username'] = user_data['username']
                st.session_state['rol'] = user_data['rol']
                st.rerun() # Recarga la app para aplicar los cambios de estado
            else:
                st.error("❌ Usuario o contraseña incorrectos.")

def logout():
    """Limpia las variables de sesión y cierra la cuenta."""
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['rol'] = ""
    st.rerun()

def main():
    """Controlador principal de la navegación."""
    # Si no está logueado, mostrar solo la pantalla de Login
    if not st.session_state['logged_in']:
        login()
    else:
        # --- BARRA LATERAL DINÁMICA ---
        st.sidebar.title(f"👋 Hola, {st.session_state['username']}")
        st.sidebar.caption(f"Rol: {st.session_state['rol']}")
        
        # Construimos el menú base
        menu = ["Dashboard"]
        
        # Agregamos opciones según el rol
        if st.session_state['rol'] in ['SuperUsuario', 'Admin']:
            menu.extend(["Clientes", "Lavadoras", "Choferes", "Servicios"])
            
        if st.session_state['rol'] == 'SuperUsuario':
            menu.extend(["Usuarios", "Auditoría Logs"])
            
        # Renderizamos el menú de radio
        opcion = st.sidebar.radio("Navegación", menu)
        
        # Botón de Cerrar Sesión
        st.sidebar.divider()
        if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
            logout()
            
        # --- ÁREA PRINCIPAL TEMPORAL ---
        st.title(f"Módulo: {opcion}")
        st.info(f"En las próximas tareas construiremos la tabla y los formularios CRUD para **{opcion}**.")

if __name__ == "__main__":
    main()