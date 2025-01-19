import streamlit as st
import threading
# app local
import data_collector
import utils

# Cargar configuraciones
iot_protocols = utils.load_json("config_iot_protocols.json")
iot_devices = utils.load_json("config_iot_devices.json")
iot_signals = utils.load_json("config_iot_signals.json")

# preprocesar configuraciones
device_data = data_collector.preprocess_configuration(iot_protocols, iot_devices, iot_signals)

# Crear hilos para cada dispositivo habilitado
for device_id in device_data:
    device_info = device_data[device_id]
    
    device = device_info["device"]
    signals = device_info["signals"]

    if (device['enabled']):
        thread = threading.Thread(target=data_collector.host_data_collection, args=(device_id, device, signals), daemon=True)
        thread.start()

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

# Interfaz de usuario
st.title("Aplicación de Lectura de Señales - Modbus TCP")

# Mostrar configuraciones cargadas
try:
    st.sidebar.write("Configuración de protocolos cargada:")
    st.sidebar.json(iot_protocols)
    st.sidebar.write("Configuración de dispositivos cargada:")
    st.sidebar.json(iot_devices)
    st.sidebar.write("Mapeo de señales cargado:")
    st.sidebar.json(iot_signals)
    st.sidebar.success("Recolección de datos en ejecución.")
except Exception as e:
    st.sidebar.error(f"Error al mostrar configuraciones: {e}")

# Manejo de cierre de conexiones
st.sidebar.button("Cerrar conexiones", on_click=data_collector.close_all_connections)
