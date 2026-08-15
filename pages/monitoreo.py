import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

# ==========================================
# 1. INICIALIZACIÓN DE DATOS EN MEMORIA (MOCK)
# ==========================================
# Usamos session_state para que la app "recuerde" los datos mientras probamos
if "alquileres_activos" not in st.session_state:
    ahora = datetime.now()
    st.session_state.alquileres_activos = [
        {"id": "SRV-001", "cliente": "Juan Pérez", "lavadora": "LAV-001", "hora_fin": ahora + timedelta(minutes=120), "saldo_extra": 0},
        {"id": "SRV-002", "cliente": "María Gómez", "lavadora": "LAV-002", "hora_fin": ahora + timedelta(minutes=15), "saldo_extra": 0},
        {"id": "SRV-003", "cliente": "Pedro Díaz", "lavadora": "LAV-003", "hora_fin": ahora - timedelta(minutes=10), "saldo_extra": 0},
    ]

def modulo_monitoreo():
    st.header("⏱️ Tablero de Monitoreo en Tiempo Real")
    st.write("Control de tiempos, alertas de retiro y gestión de horas extra.")

    # ==========================================
    # 2. MOTOR DE TIEMPO Y COLORES (TABLERO)
    # ==========================================
    ahora_actual = datetime.now()
    
    col_verde, col_amarilla, col_roja = st.columns(3)
    
    with col_verde:
        st.success("🟢 **En Curso (> 30 min)**")
    with col_amarilla:
        st.warning("🟡 **Alerta (<= 30 min)**")
    with col_roja:
        st.error("🔴 **Vencido / Por Retirar**")

    st.markdown("---")

    # Recorremos cada alquiler activo para calcular su estado en vivo
    for idx, alquiler in enumerate(st.session_state.alquileres_activos):
        tiempo_restante = alquiler["hora_fin"] - ahora_actual
        minutos_restantes = int(tiempo_restante.total_seconds() / 60)

        # Lógica estricta de colores según tus requerimientos
        if minutos_restantes > 30:
            color = "🟢"
            estado_texto = f"Restan {minutos_restantes} min"
            alerta = st.success
        elif 0 < minutos_restantes <= 30:
            color = "🟡"
            estado_texto = f"¡ALERTA! Restan {minutos_restantes} min"
            alerta = st.warning
        else:
            color = "🔴"
            minutos_vencidos = abs(minutos_restantes)
            estado_texto = f"VENCIDO hace {minutos_vencidos} min"
            alerta = st.error

        # Dibujamos la tarjeta visual del alquiler
        alerta(f"""
        **{color} {alquiler['lavadora']} - {alquiler['cliente']}**  
        ⏳ Estado: {estado_texto} | ⏰ Fin programado: {alquiler['hora_fin'].strftime('%I:%M %p')}  
        💵 Saldo Extra Acumulado: **${alquiler['saldo_extra']}**
        """)

    st.markdown("---")

    # ==========================================
    # 3. MÓDULO DE EXTENSIONES Y HORAS EXTRA
    # ==========================================
    st.subheader("⏳ Gestionar Extensiones de Tiempo")
    
    with st.form("form_extensiones"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Selector de alquiler a extender
            opciones_alquiler = [f"{a['id']} - {a['cliente']}" for a in st.session_state.alquileres_activos]
            seleccion = st.selectbox("Seleccionar Servicio", opciones_alquiler)
        
        with col2:
            # Tipos de extensión
            tipo_extension = st.selectbox("Tiempo Extra", [
                "+1 Hora ($2)", 
                "+2 Horas ($4)", 
                "Extensión Nocturna / 12h ($6)", 
                "Extensión 24h ($12)"
            ])
            
        with col3:
            metodo_pago_ext = st.selectbox("Método de Pago", ["Efectivo USD", "Pago Móvil", "Añadir a Deuda"])

        btn_extender = st.form_submit_button("➕ Aplicar Extensión y Recalcular", type="primary")

        if btn_extender:
            # Lógica matemática de tarifas y tiempos
            minutos_extra = 0
            costo_extra = 0
            
            if "+1 Hora" in tipo_extension:
                minutos_extra = 60
                costo_extra = 2
            elif "+2 Horas" in tipo_extension:
                minutos_extra = 120
                costo_extra = 4
            elif "12h" in tipo_extension:
                minutos_extra = 12 * 60
                costo_extra = 6
            elif "24h" in tipo_extension:
                minutos_extra = 24 * 60
                costo_extra = 12

            # Buscamos el alquiler seleccionado en la memoria y lo actualizamos
            id_seleccionado = seleccion.split(" - ")[0]
            for alq in st.session_state.alquileres_activos:
                if alq["id"] == id_seleccionado:
                    alq["hora_fin"] += timedelta(minutes=minutos_extra)
                    if "Añadir a Deuda" in metodo_pago_ext:
                        alq["saldo_extra"] += costo_extra
                    break
            
            st.success(f"✅ ¡Tiempo extendido! Se sumaron {minutos_extra/60} horas a {seleccion}.")
            time.sleep(1.5) # Pequeña pausa para que el usuario lea el éxito
            st.rerun() # FORZAMOS EL REFRESCO para actualizar los colores inmediatamente

    # ==========================================
    # 4. HILO DE REFRESCO AUTOMÁTICO (LIVE REFRESH)
    # ==========================================
    st.sidebar.markdown("### ⚙️ Motor en Vivo")
    auto_refresh = st.sidebar.checkbox("Activar Auto-Refresco (60s)", value=False)
    
    if auto_refresh:
        st.sidebar.info("El tablero se actualizará solo en 60 segundos...")
        time.sleep(60)
        st.rerun()

# === INICIO DE LA APP ===
if __name__ == "__main__":
    modulo_monitoreo()