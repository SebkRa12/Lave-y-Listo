import streamlit as st
from datetime import date

def modulo_agendamiento():
    st.header("🗓️ Agendamiento de Servicios")
    st.write("Central de mando para coordinar nuevos alquileres y despachos rápidos.")

    with st.form("form_nuevo_servicio", clear_on_submit=True):
        st.subheader("Nuevo Alquiler")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cliente = st.selectbox("1. Seleccionar Cliente", ["Juan Pérez (Centro)", "María Gómez (Los Olivos)"])
            # Actualizado con tus capacidades reales
            lavadora = st.selectbox("2. Lavadora Disponible", ["LAV-001 (12 kg)", "LAV-002 (16 kg)"])
            chofer = st.selectbox("3. Chofer Libre", ["Carlos Rodríguez (Toyota Hilux)"])
            fecha = st.date_input("Fecha del Servicio", value=date.today())
            
        with col2:
            # === HORARIOS FIJOS BASADOS EN TU CATÁLOGO ===
            turno = st.selectbox("Turno de Alquiler", [
                "Mañana (6:00 am a 1:00 pm)", 
                "Tarde (1:30 pm a 7:00 pm)", 
                "Día Completo (6:00 am a 7:00 pm)", 
                "Nocturno (8:00 pm a 6:00 am)",
                "24h Oferta"
            ])
            
            # === TARIFADOR AUTOMÁTICO EXACTO ===
            monto_calculado = 0
            if "Mañana" in turno:
                monto_calculado = 7
            elif "Tarde" in turno or "Nocturno" in turno:
                monto_calculado = 6
            elif "Día Completo" in turno or "24h" in turno:
                monto_calculado = 12
                
            # Métodos de pago adaptados a tu negocio
            metodo_pago = st.selectbox("Método de Pago", [
                "Efectivo USD", 
                "Pago Móvil (Bs a tasa BCV)", 
                "Efectivo Bs", 
                "Pendiente por Cobrar"
            ])
            
            # === LÓGICA INTELIGENTE DE DESCUENTO ===
            descuento = 0
            # Si eligen efectivo, mostramos la opción de descuento promocional
            if "Efectivo USD" in metodo_pago:
                aplicar_descuento = st.checkbox("💸 Aplicar descuento por pago en efectivo")
                if aplicar_descuento:
                    # Permite elegir cuánto descontar (por defecto $1)
                    descuento = st.number_input("Monto a descontar ($)", min_value=0, max_value=monto_calculado, value=1)
            
            total_final = monto_calculado - descuento
            st.info(f"💵 Tarifa Final: **${total_final} USD**")

        st.markdown("---")
        st.markdown("### ⚠️ Validaciones Críticas de Operación")
        
        confirmacion_servicios = st.checkbox(
            "✅ Confirmación Previa de Agua y Luz (Llamar al cliente 30 min antes)",
            help="Obligatorio marcar para poder registrar el servicio."
        )

        submit_btn = st.form_submit_button("🚀 Procesar Agendamiento", type="primary")

        if submit_btn:
            if not confirmacion_servicios:
                st.error("🛑 ALERTA: Operación bloqueada. Debes confirmar telefónicamente que el cliente tiene agua y electricidad antes de despachar la máquina.")
            else:
                st.success(f"✅ ¡Servicio de {turno} agendado con éxito para {cliente} por un total de ${total_final}!")
                st.balloons()

# === INICIO DE LA APP (AISLADO) ===
if __name__ == "__main__":
    modulo_agendamiento()