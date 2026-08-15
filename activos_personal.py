import streamlit as st
import pandas as pd

def modulo_activos_personal():
    st.header("⚙️ Gestión de Activos y Personal")
    st.write("Control de inventario de lavadoras, mantenimiento y asignación de vehículos.")

    # Separamos en dos grandes bloques
    tab_lavadoras, tab_choferes = st.tabs(["🧺 Lavadoras", "🚚 Choferes"])

    # ==========================================
    # PESTAÑA 1: GESTIÓN DE LAVADORAS
    # ==========================================
    with tab_lavadoras:
        st.subheader("Inventario y Mantenimiento")
        
        # Usamos un expander para ocultar el formulario y no saturar la pantalla
        with st.expander("➕ Registrar Nueva Lavadora"):
            with st.form("form_registro_lavadora", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    marca = st.text_input("Marca y Modelo *")
                    capacidad = st.number_input("Capacidad (Kg) *", min_value=5, max_value=30, value=12)
                with col2:
                    bomba = st.selectbox("Tipo de Bomba", ["Drenaje Automático", "Gravedad"])
                    estatus_inicial = st.selectbox("Estatus Inicial", ["Disponible", "Mantenimiento"])
                
                submit_lavadora = st.form_submit_button("💾 Guardar Lavadora", type="primary")
                if submit_lavadora:
                    if not marca:
                        st.error("⚠️ El campo Marca y Modelo es obligatorio.")
                    else:
                        st.success(f"✅ Lavadora {marca} de {capacidad}kg registrada exitosamente.")

        st.markdown("### Panel de Control de Equipos")
        st.info("💡 Los equipos con 50 ciclos o más requieren mantenimiento preventivo.")
        
        # --- DATOS MOCK DE LAVADORAS ---
        datos_lavadoras = pd.DataFrame({
            "Código ID": ["LAV-001", "LAV-002", "LAV-003", "LAV-004"],
            "Marca": ["LG Tromm", "Samsung", "Mabe", "Whirlpool"],
            "Capacidad (Kg)": [12, 15, 10, 18],
            "Estatus": ["Disponible", "Alquilada", "Mantenimiento", "Disponible"],
            "Ciclos de Lavado": [15, 48, 120, 51] # 51 y 120 son alertas
        })

        # Configuramos la tabla interactiva
        df_editado_lav = st.data_editor(
            datos_lavadoras,
            use_container_width=True,
            num_rows="dynamic",
            column_config={
                "Código ID": st.column_config.TextColumn("Código ID", disabled=True),
                "Marca": st.column_config.TextColumn("Marca", disabled=True),
                "Estatus": st.column_config.SelectboxColumn(
                    "Estatus Actual",
                    options=["Disponible", "Alquilada", "Mantenimiento"],
                    required=True
                ),
                "Ciclos de Lavado": st.column_config.NumberColumn(
                    "Contador de Ciclos",
                    help="Suma 1 automáticamente por cada alquiler."
                )
            },
            key="editor_lavadoras"
        )
        
        if st.button("🔄 Guardar Cambios de Equipos"):
            st.success("Estatus de lavadoras actualizado en la base de datos.")

    # ==========================================
    # PESTAÑA 2: GESTIÓN DE CHOFERES
    # ==========================================
    with tab_choferes:
        st.subheader("Directorio de Choferes y Vehículos")
        
        with st.expander("➕ Registrar Nuevo Chofer"):
            with st.form("form_registro_chofer", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    nombre_chofer = st.text_input("Nombre Completo *")
                    tel_chofer = st.text_input("Teléfono *")
                with col2:
                    vehiculo = st.text_input("Vehículo (Ej: Pick-Up Ford) *")
                    placa = st.text_input("Placa *")
                
                submit_chofer = st.form_submit_button("💾 Guardar Chofer", type="primary")
                if submit_chofer:
                    if not (nombre_chofer and vehiculo and placa):
                        st.error("⚠️ Faltan campos obligatorios.")
                    else:
                        st.success(f"✅ Chofer {nombre_chofer} registrado exitosamente.")

        st.markdown("### Asignación Operativa")
        
        # --- DATOS MOCK DE CHOFERES ---
        datos_choferes = pd.DataFrame({
            "ID": [1, 2],
            "Nombre": ["Carlos Rodríguez", "Miguel Torres"],
            "Teléfono": ["0414-9876543", "0424-1234567"],
            "Vehículo": ["Toyota Hilux", "Chevrolet LUV"],
            "Placa": ["A12B34C", "X98Y76Z"],
            "Estatus": ["Activo", "Inactivo"]
        })

        df_editado_chof = st.data_editor(
            datos_choferes,
            use_container_width=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "Estatus": st.column_config.SelectboxColumn(
                    "Estatus",
                    options=["Activo", "Inactivo", "En Ruta"],
                    required=True
                )
            },
            key="editor_choferes"
        )

        if st.button("🔄 Guardar Cambios de Personal"):
            st.success("Datos de choferes actualizados en la base de datos.")

# === INICIO DE LA APP (AISLADO) ===
if __name__ == "__main__":
    modulo_activos_personal()
    