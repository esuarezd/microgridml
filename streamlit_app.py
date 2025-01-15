import streamlit as st
import pandas as pd
from data_collect import load_json, update_devices_status

# Cargar dispositivos IoT y protocolos
iot_devices = load_json("iot_devices.json")
protocols = load_json("protocols.json")

# Configuración de la página
st.set_page_config(
    layout="wide",  
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

# Menú de navegación
menu = st.sidebar.selectbox(
    "Menú",
    options=["Home", "Comm"],
    index=0
)

if menu == "Home":
    st.title("Home - Datos de los Dispositivos IoT")
    st.write("Próximamente se mostrarán los datos leídos de los dispositivos.")
    
elif menu == "Comm":
    st.title("Comm - Estado de Comunicaciones")
    st.subheader("Estado de los Dispositivos IoT")

    # Actualizar el estado de los dispositivos
    update_devices_status(iot_devices, protocols)

    # Crear columnas dinámicas
    for device in iot_devices:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # Casilla de habilitación
            device["enabled"] = st.checkbox(
                f"Activar {device['device_name']}",
                value=device["enabled"]
            )
        with col2:
            st.write(device["device_name"])
        with col3:
            st.write(device["ip_address"])
        with col4:
            st.write(device["protocol_name"])
        with col5:
            # Mostrar estado de conexión
            status_color = (
                "green" if device["connection_status"] == "OK" else
                "red" if device["connection_status"] == "Failure" else
                "gray"
            )
            st.markdown(
                f"<span style='color: {status_color}; font-weight: bold;'>{device['connection_status']}</span>",
                unsafe_allow_html=True
            )