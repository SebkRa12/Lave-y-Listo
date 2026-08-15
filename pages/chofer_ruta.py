import streamlit as st
import urllib.parse

def modulo_chofer_ruta():
    # Estilo visual limpio y optimizado para pantallas de teléfonos móviles
    st.markdown("<h2 style='text-align: center;'>🚚 Mi Ruta del Día</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Panel exclusivo para el repartidor en calle</p>", unsafe_allow_html=True)
    
    # Identificación rápida del chofer en sesión
    st.info("👤 Chofer: **Carlos Rodríguez** | 🚙 Vehículo: Toyota Hilux")
    st.markdown("---")
    
    # Inicializamos las rutas en memoria de sesión para hacerlas interactivas
    if "rutas_chofer" not in st.session_state:
        st.session_state.rutas_chofer = [
            {
                "id": "SRV-001",
                "cliente": "Juan Pérez",
                "telefono": "04141234567",
                "sector": "Centro",
                "direccion": "Calle Bolívar, Casa Nro. 45",
                "referencia": "Al lado de la panadería La Espiga",
                "tipo": "Entrega de Lavadora",
                "lavadora": "LAV-001 (12 kg)",
                "estado_operativo": "En Camino 🚗"
            },
            {
                "id": "SRV-002",
                "cliente": "María Gómez",
                "telefono": "04247654321",
                "sector": "Los Olivos",
                "direccion": "Urbanización Los Olivos, Manzana 12, Casa 8",
                "referencia": "Frente al parque infantil (Casa reja blanca)",
                "tipo": "Retiro de Lavadora",
                "lavadora": "LAV-002 (16 kg)",
                "estado_operativo": "Pendiente de Salida 🕒"
            }
        ]
    
    if not st.session_state.rutas_chofer:
        st.success("🎉 ¡Buen trabajo! No tienes servicios pendientes en este momento.")
        return

    # Renderizamos cada servicio en forma de tarjeta interactiva
    for idx, ruta in enumerate(st.session_state.rutas_chofer):
        with st.container():
            st.markdown(f"### 📦 {ruta['id']} [{ruta['tipo']}]")
            st.write(f"🏷️ **Estatus Actual:** `{ruta['estado_operativo']}` | 🧺 **Máquina:** {ruta['lavadora']}")
            st.write(f"📍 **Sector:** {ruta['sector']}")
            st.write(f"👤 **Cliente:** {ruta['cliente']}")
            st.write(f"🏠 **Dirección:** {ruta['direccion']}")
            st.write(f"📌 **Referencia:** {ruta['referencia']}")
            
            # Limpieza y formateo del número para llamadas y WhatsApp directo
            telefono_limpio = "".join(filter(str.isdigit, ruta['telefono']))
            if telefono_limpio.startswith("0"):
                telefono_limpio = "58" + telefono_limpio[1:]
            elif not telefono_limpio.startswith("58"):
                telefono_limpio = "58" + telefono_limpio
            
            # Construcción del enlace de Google Maps
            texto_busqueda = f"{ruta['direccion']}, {ruta['sector']}, Maturin"
            maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(texto_busqueda)}"
            
            # Fila de botones de contacto y ubicación
            col_llamada, col_wa, col_maps = st.columns(3)
            with col_llamada:
                st.link_button("📞 Llamar", f"tel:+{telefono_limpio}", use_container_width=True)
            with col_wa:
                st.link_button("💬 WhatsApp", f"https://wa.me/{telefono_limpio}?text=Hola%20{ruta['cliente']},%20somos%20de%20Lave%20y%20Listo,%20estamos%20en%20camino.", use_container_width=True)
            with col_maps:
                st.link_button("🗺️ Mapa", maps_url, use_container_width=True)
            
            # --- TAREA 4.2: BOTONES DE ACCIÓN OPERATIVA RÁPIDA ---
            st.markdown("#### ⚡ Acciones Operativas en Puerta")
            col_sitio, col_entregado, col_retirado = st.columns(3)
            
            with col_sitio:
                if st.button("⏱️ En Sitio", key=f"sitio_{idx}", use_container_width=True):
                    st.session_state.rutas_chofer[idx]["estado_operativo"] = "En Puerta (Tolerancia 15 min) ⏱️"
                    st.toast(f"⏱️ Cronómetro de 15 min iniciado para {ruta['cliente']}.")
                    st.rerun()
                    
            with col_entregado:
                if st.button("🧼 Entregado", key=f"ent_{idx}", use_container_width=True):
                    st.session_state.rutas_chofer[idx]["estado_operativo"] = "Entregado y Activo 🧼"
                    st.toast(f"🧼 ¡Servicio registrado! Temporizador central activado.")
                    st.rerun()
                    
            with col_retirado:
                if st.button("🚚 Retirado", key=f"ret_{idx}", use_container_width=True):
                    st.session_state.rutas_chofer[idx]["estado_operativo"] = "Finalizado / Lavadora Libre ✅"
                    st.toast(f"🚚 Lavadora {ruta['lavadora']} liberada con éxito.")
                    st.rerun()
            
            st.markdown("---")

# === INICIO DE LA APP ===
if __name__ == "__main__":
    modulo_chofer_ruta()