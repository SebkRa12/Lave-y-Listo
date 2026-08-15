import streamlit as st
import pandas as pd
import sqlite3
import os

# Asegurarnos de que exista la carpeta para las fotos de las cédulas
UPLOAD_DIR = "uploads/cedulas"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def guardar_foto_cedula(foto_archivo, cedula):
    """Guarda el archivo subido y retorna la ruta."""
    if foto_archivo is not None:
        file_extension = foto_archivo.name.split(".")[-1]
        file_path = f"{UPLOAD_DIR}/{cedula}.{file_extension}"
        with open(file_path, "wb") as f:
            f.write(foto_archivo.getbuffer())
        return file_path
    return None

def modulo_clientes():
    st.header("👥 Gestión de Clientes")
    st.write("Administra el directorio, registra nuevos usuarios y actualiza clasificaciones.")

    # Usamos pestañas para separar la creación de la edición
    tab_nuevo, tab_directorio = st.tabs(["➕ Registrar Cliente", "📋 Directorio y Edición Rápida"])

    # ==========================================
    # PESTAÑA 1: FORMULARIO DE ALTA
    # ==========================================
    with tab_nuevo:
        with st.form("form_registro_cliente", clear_on_submit=True):
            st.subheader("Datos del Nuevo Cliente")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre Completo *")
                cedula = st.text_input("Cédula *")
                telefono1 = st.text_input("Teléfono 1 (Principal/WhatsApp) *")
                telefono2 = st.text_input("Teléfono 2 (Opcional)")
                
            with col2:
                sector = st.text_input("Sector *")
                direccion = st.text_area("Dirección Exacta *")
                referencia = st.text_input("Punto de Referencia")
                # El selector manual de clasificación
                clasificacion = st.selectbox(
                    "Clasificación Inicial", 
                    options=["Nuevo", "Frecuente", "VIP", "Lista Negra"]
                )
            
            foto_cedula = st.file_uploader("Foto de Cédula (Opcional)", type=["jpg", "jpeg", "png"])
            
            st.markdown("*Campos obligatorios")
            submit_btn = st.form_submit_button("💾 Guardar Cliente", type="primary")

            if submit_btn:
                if not (nombre and cedula and telefono1 and sector and direccion):
                    st.error("⚠️ Por favor, completa todos los campos obligatorios.")
                else:
                    # Aquí procesamos la imagen
                    ruta_foto = guardar_foto_cedula(foto_cedula, cedula)
                    
                    # TODO: Aquí llamarías a tu función de database.py para hacer el INSERT
                    # database.insertar_cliente(nombre, cedula, ruta_foto, telefono1, telefono2, sector, direccion, referencia, clasificacion)
                    
                    st.success(f"✅ Cliente {nombre} registrado exitosamente.")

    # ==========================================
    # PESTAÑA 2: TABLA INTERACTIVA (EDICIÓN RÁPIDA)
    # ==========================================
    with tab_directorio:
        st.subheader("Directorio (Edición en vivo)")
        st.info("💡 Haz doble clic en cualquier celda para editar (ej: corregir un teléfono o cambiar la clasificación).")
        
        # TODO: Aquí llamas a tu BD para traer los clientes reales
        # conn = sqlite3.connect("lave_y_listo.db")
        # df_clientes = pd.read_sql("SELECT ID, Nombre, Cédula, Teléfonos_1, Sector, Clasificación FROM clientes", conn)
        
        # --- DATOS DE PRUEBA (MOCK) MIENTRAS CONECTAS LA BD ---
        datos_prueba = pd.DataFrame({
            "ID": [1, 2],
            "Nombre": ["Juan Pérez", "María Gómez"],
            "Cédula": ["V-12345678", "V-87654321"],
            "Teléfono": ["0414-1234567", "0424-7654321"],
            "Sector": ["Centro", "Los Olivos"],
            "Clasificación": ["Frecuente", "Nuevo"]
        })
        # --------------------------------------------------------

        # Configuramos st.data_editor para que ciertos campos sean editables y otros no
        df_editado = st.data_editor(
            datos_prueba,
            use_container_width=True,
            num_rows="dynamic", # Permite agregar o borrar filas desde la interfaz
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True), # El ID no se debe editar
                "Clasificación": st.column_config.SelectboxColumn(
                    "Clasificación",
                    options=["Nuevo", "Frecuente", "VIP", "Lista Negra"],
                    required=True
                )
            },
            key="editor_clientes" # Clave única requerida por Streamlit
        )

        # Botón para confirmar los cambios masivos en la base de datos
        if st.button("🔄 Guardar Cambios del Directorio"):
            # TODO: Lógica para iterar df_editado y hacer UPDATE en SQLite
            # Y registrar en la tabla auditoria_logs (Sprint 1)
            st.success("Cambios actualizados en la base de datos.")
if __name__ == "__main__":
    modulo_clientes()