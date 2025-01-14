import streamlit as st
from config_loader import load_config
#from modbus import data_collect

# Configuración de la página para usar todo el ancho disponible
st.set_page_config(
    layout="wide",  
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

st.title("Aplicación Streamlit en Raspberry Pi")
st.write("Hola, esta es mi primera aplicación web con Streamlit en la Raspberry Pi.")

iot_devices = load_config("config_iot_devices.json")

# Configuración de dispositivos
for device in iot_devices:
    col1, col2 = st.columns(2)
    with col1:
        device["enabled"] = st.checkbox(f"Activar {device['device_name']} ({device['ip_address']})", value=device["enabled"])
    with col2:
        device["poll_rate_min"] = st.number_input(
            f"Polling Rate para {device['device_name']} (minutos)",
            min_value=1,
            value=device["poll_rate_min"]
        )


# data = data_collect(iot_devices)