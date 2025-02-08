import pandas as pd
import streamlit as st
import logging
import time
import sys
import os
# Agregar la ruta de la raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import app.visualization.logic as logic

# Definir la ruta del directorio de logs 
log_file = 'logs/visualization/view.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

def new_iot_system():
    app = logic.new_iot_system()
    return app

def load_data(app):
    logic.load_data(app)

def connect_to_realtime_data():
    realtime_data = logic.connect_to_realtime_data()
    return realtime_data

def build_devices_list(app):
    iot_devices = app["devices"]
    devices = iot_devices.get("elements")
    iot_protocols = app["protocols"]
    protocols = iot_protocols.get('elements')
    # Crear un diccionario de protocolos para mapear fácilmente
    protocol_dict = {protocol["protocol_id"]: protocol["protocol_name"] for protocol in protocols}

    # Extraer los datos que queremos y agregar el protocol_name
    output = []
    for device in devices:
        # Crear el nuevo diccionario con los campos deseados
        device_info = {
            "enabled": device["enabled"],
            "device_name": device["device_name"],
            "host": device["host"],
            "unit_id": device["unit_id"],
            "unit_name": device["unit_name"],
            "protocol_name": protocol_dict.get(device["protocol_id"], "Unknown")  # Buscar el nombre del protocolo
        }
        output.append(device_info)
    
    return output

def build_group_1_list(realtime_data):
    iot_signals = app["signals"]
    signals = iot_signals["elements"]
    data_list = []
    for signal in realtime_data.values():
        data_list.append({
            "signal_id":signal.get('signal_id'),
            "group_id": signal.get('group_id'),
            "device_id": signal.get('device_id'),
            "value protocol": signal.get('value_protocol'),
            "value data type": signal.get('value_data_type'),
            "value": signal.get('value'),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(signal.get('timestamp')))
        })
    return data_list

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

try:
    app = new_iot_system()
    load_data(app)
    realtime_data = connect_to_realtime_data()

except Exception as e:
    st.error(f"Error conectando a datos en tiempo real: {e}")
    logging.error(f"view: Error conectando a datos en tiempo real: {e}")
    

# Inicializar el estado de navegación
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Sidebar con botones para navegar
if st.sidebar.button("home"):
    st.session_state["page"] = "home"
if st.sidebar.button("realtime"):
    st.session_state["page"] = "realtime"
if st.sidebar.button("history"):
    st.session_state["page"] = "history"
if st.sidebar.button("devices"):
    st.session_state["page"] = "devices"
    
# Navegación entre páginas
if st.session_state["page"] == "home":
    st.title("Microgrid ML")
    st.write("Sistema IoT en ejecución.")

if st.session_state["page"] == "realtime":
    st.title("Microgrid ML")
    st.write("Datos de tiempo real")
    # Lista de llaves que deseas mostrar
    group_1_list = build_group_1_list(app)
    
    df_group_1 = pd.DataFrame(group_1_list)
    st.dataframe(df_group_1) 

elif st.session_state["page"] == "history":
    st.title("Microgrid ML")
    st.write("Historial de lecturas de señales (en desarrollo).")

elif st.session_state["page"] == "devices":
    st.title("Microgrid ML")
    st.write("Equipos IoT del sistema.")
    
    # Lista de llaves que deseas mostrar
    devices_list = build_devices_list(app)
    
    df_devices = pd.DataFrame(devices_list)
    st.dataframe(df_devices)