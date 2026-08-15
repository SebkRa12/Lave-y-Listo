import streamlit as st
import urllib.parse

def generar_enlace_wa(telefono, mensaje):
    """Genera el enlace directo a WhatsApp con el mensaje codificado."""
    # Limpiamos el teléfono de espacios o guiones
    telefono_limpio = "".join(filter(str.isdigit, telefono))
    
    # Adaptación automática para números de Venezuela (Cambia el 0 inicial por 58)
    if telefono_limpio.startswith("0"):
        telefono_limpio = "58" + telefono_limpio[1:]
    elif not telefono_limpio.startswith("58"):
        telefono_limpio = "58" + telefono_limpio
        
    # Codificamos el mensaje para que WhatsApp respete los saltos de línea y emojis
    mensaje_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/{telefono_limpio}?text={mensaje_codificado}"

def modulo_whatsapp():
    st.header("💬 Generador de Plantillas de WhatsApp")
    st.write("Automatiza la comunicación con tus clientes enviando mensajes estandarizados.")

    tab_reserva, tab_encuesta = st.tabs(["✅ Reserva Confirmada", "⭐ Encuesta de Satisfacción"])

    # ==========================================
    # PESTAÑA 1: RESERVA CONFIRMADA
    # ==========================================
    with tab_reserva:
        st.subheader("Enviar Confirmación de Alquiler")
        
        col1, col2 = st.columns(2)
        with col1:
            cliente_nombre = st.text_input("Nombre del Cliente", value="Juan Pérez")
            # El teléfono se puede ingresar con o sin el cero inicial
            telefono_cliente = st.text_input("Teléfono del Cliente (Ej: 04241234567)", key="tel_reserva")
        
        with col2:
            turno_reservado = st.selectbox("Turno a confirmar", [
                "Mañana (6:00 am a 1:00 pm)", 
                "Tarde (1:30 pm a 7:00 pm)", 
                "Día Completo (6:00 am a 7:00 pm)", 
                "Nocturno (8:00 pm a 6:00 am)",
                "24h Oferta"
            ])
            monto_total = st.number_input("Monto Total Acordado ($)", value=7)

        # Plantilla del mensaje inyectando las variables y tu identidad gráfica
        mensaje_reserva = f"""¡Hola {cliente_nombre}! 👋🏼
Gracias por elegirnos. Confirmamos su reserva con *_Lave y Listo_* 👚👕

🗓️ *Detalles de su servicio:*
⏱️ Turno: {turno_reservado}
💵 Total a pagar: ${monto_total}
🚚 Le llevaremos la lavadora hasta la puerta de su 🏠.

⚠️ *Recuerde:* Nuestro chofer le contactará 30 minutos antes para confirmar que cuenta con servicio de agua y electricidad. 

¡Suelte ese manduco! 🤗"""

        st.markdown("**Vista previa del mensaje:**")
        st.info(mensaje_reserva)

        if telefono_cliente:
            enlace_wa = generar_enlace_wa(telefono_cliente, mensaje_reserva)
            # st.link_button abre directamente la app de WhatsApp o WhatsApp Web
            st.link_button("📲 Abrir en WhatsApp y Enviar Confirmación", enlace_wa, type="primary")
        else:
            st.warning("⚠️ Ingresa un número de teléfono válido para habilitar el botón de envío.")

    # ==========================================
    # PESTAÑA 2: ENCUESTA DE SATISFACCIÓN
    # ==========================================
    with tab_encuesta:
        st.subheader("Enviar Encuesta Post-Servicio")
        
        tel_encuesta = st.text_input("Teléfono del Cliente", key="tel_encuesta")
        
        mensaje_encuesta = """¡Hola! 👋🏼 Esperamos que haya tenido una excelente experiencia con *_Lave y Listo_* 👚👕.

Para nosotros es muy importante mejorar cada día. ¿Cómo calificaría nuestro servicio de hoy?

Responda con un número del 1 al 5:
⭐ (Malo)
⭐⭐ (Regular)
⭐⭐⭐ (Bueno)
⭐⭐⭐⭐ (Muy Bueno)
⭐⭐⭐⭐⭐ (¡Excelente!)

¡Agradecemos mucho su confianza! 🙏🏼"""

        st.markdown("**Vista previa del mensaje:**")
        st.success(mensaje_encuesta)

        if tel_encuesta:
            enlace_encuesta = generar_enlace_wa(tel_encuesta, mensaje_encuesta)
            st.link_button("📲 Abrir en WhatsApp y Enviar Encuesta", enlace_encuesta, type="primary")
        else:
            st.warning("⚠️ Ingresa un número de teléfono válido para habilitar el botón de envío.")

# === INICIO DE LA APP ===
if __name__ == "__main__":
    modulo_whatsapp()
    