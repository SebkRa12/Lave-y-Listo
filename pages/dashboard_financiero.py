import streamlit as st
import pandas as pd
import datetime

def modulo_financiero():
    st.set_page_config(layout="wide") # Dashboard requiere espacio
    st.header("📊 Dashboard Financiero y Auditoría")
    
    # 1. DATOS SIMULADOS (Esto luego vendrá de tu BD SQL)
    data_ingresos = pd.DataFrame({
        'Fecha': ['2026-08-10', '2026-08-11', '2026-08-12', '2026-08-13'],
        'USD': [45, 60, 30, 55],
        'Bs': [1200, 1500, 800, 1300]
    })
    
    data_maquinas = pd.DataFrame({
        'Lavadora': ['LAV-001', 'LAV-002', 'LAV-003', 'LAV-004'],
        'Horas': [15, 22, 10, 5],
        'Ingresos_USD': [120, 180, 80, 40]
    })
    
    # 2. KPIs (Indicadores Clave)
    col1, col2, col3 = st.columns(3)
    col1.metric("Ingreso Total (USD)", f"${data_ingresos['USD'].sum()}", "+12%")
    col2.metric("Ingreso Total (Bs)", f"Bs {data_ingresos['Bs'].sum()}", "-5%")
    col3.metric("Servicios Activos", "12", "En curso")

    st.markdown("---")

    # 3. GRÁFICOS INTERACTIVOS
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Tendencia de Ingresos (USD)")
        st.bar_chart(data_ingresos.set_index('Fecha')['USD'])
        
    with col_chart2:
        st.subheader("Productividad por Máquina")
        st.bar_chart(data_maquinas.set_index('Lavadora')['Ingresos_USD'])

    st.markdown("---")

    # 4. VISOR DE LOGS DE AUDITORÍA (Crucial para seguridad)
    st.subheader("🕵️‍♂️ Registro de Auditoría")
    
    logs = [
        {"Fecha": "2026-08-14 10:00", "Usuario": "Admin", "Acción": "Editó tarifa LAV-002"},
        {"Fecha": "2026-08-14 11:30", "Usuario": "Chofer_Carlos", "Acción": "Marcó 'Retirado' SRV-001"},
        {"Fecha": "2026-08-14 14:15", "Usuario": "Admin", "Acción": "Eliminó registro erróneo SRV-000"},
    ]
    
    df_logs = pd.DataFrame(logs)
    st.dataframe(df_logs, use_container_width=True)

# === INICIO ===
if __name__ == "__main__":
    modulo_financiero()
    