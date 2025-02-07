import pandas as pd
import streamlit as st
import json
import logging
import time
import os
from multiprocessing.managers import BaseManager

# local import

# Verificar si la carpeta 'logs' existe, si no, crearla
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler("logs/streamlit_app.log", mode="a")  # Registrar en un archivo
    ]
)

class RealtimeDataManager(BaseManager):
    pass

# Registrar el diccionario compartido
RealtimeDataManager.register('get_realtime_data')

def connect_to_realtime_data():
    """Conectar al diccionario de datos en tiempo real."""
    try:
        manager = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
        manager.connect()
        logging.info("Conectado al backend de datos en tiempo real.")
        manager_data = manager.get_realtime_data()
        logging.info("Leyendo multiprocess basemanager:", type(manager_data))
        realtime_data = manager_data.copy()
        return realtime_data
    except Exception as e:
        logging.error(f"Error conectando a datos en tiempo real: {e}")
        return None

    
# Cargar configuraciones de señales y grupos
with open('data/config_iot/devices.json') as f:
    config_iot_devices = json.load(f)

with open('data/config_iot/protocols.json') as f:
    config_iot_protocols = json.load(f)

with open('data/config_iot/signals.json') as f:
    config_iot_signals = json.load(f)

with open('data/config_iot/groups.json') as f:
    config_signals_group = json.load(f)

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

# Conexión al backend
try:
    realtime_data = connect_to_realtime_data()

except Exception as e:
    st.error(f"Error conectando a datos en tiempo real: {e}")
    logging.error(f"Error conectando a datos en tiempo real: {e}")

# Inicializar el estado de navegación
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Sidebar con botones para navegar
if st.sidebar.button("Home"):
    st.session_state["page"] = "Home"
if st.sidebar.button("Realtime"):
    st.session_state["page"] = "Realtime"
if st.sidebar.button("History"):
    st.session_state["page"] = "History"
if st.sidebar.button("Devices"):
    st.session_state["page"] = "Devices"

# Navegación entre páginas
if st.session_state["page"] == "Home":
    st.title("Microgrid ML")
    st.write("Sistema IoT en ejecución.")
    # Convertir realtime_data a un diccionario regular antes de mostrarlo
    if realtime_data:
        st.write("Datos en tiempo real", realtime_data)  # Mostrar los datos recibidos
    
    # Configurar actualización periódica (actualiza cada 10 segundos)
    time.sleep(60)  # pausa en segundos
    st.rerun()

if st.session_state["page"] == "Realtime":
    st.title("Microgrid ML")
    st.write("Datos de tiempo real. version 4-feb-2025 8:35 am")
    placeholder = st.empty()  # Reservar espacio para la tabla de señales

    while True:
        # Construcción de la tabla de tiempo real
        data_list = []
        for signal in realtime_data:
            data_list.append({
                "signal_id":signal.get('signal_id'),
                "group_id": signal.get('group_id'),
                "device_id": signal.get('device_id'),
                "value protocol": signal.get('value_protocol'),
                "value data type": signal.get('value_data_type'),
                "value": signal.get('value'),
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(signal.get('timestamp')))
            })
        df = pd.DataFrame(data_list)
        placeholder.dataframe(df)

        time.sleep(60)  
    


elif st.session_state["page"] == "History":
    st.title("Microgrid ML")
    st.write("Historial de lecturas de señales (en desarrollo).")

elif st.session_state["page"] == "Devices":
    st.title("Microgrid ML")
    st.write("Estado comunicación de los Dispositivos IoT (Versión 1-Feb 9:23 pm)")
    data_list = []
    for device in config_iot_devices:
        protocol_name = next((m["protocol_name"] for m in config_iot_protocols if m["protocol_id"] == device["protocol_id"]), "Unknown")
        data_list.append({
            "enabled": device.get('enabled'),
            "device name": device.get('device_name'),
            "host": device.get('host'),
            "protocol": protocol_name,
            "unit_id": device.get('unit_id'),
            "unit name": device.get('unit_name')
        })
    df = pd.DataFrame(data_list)
    st.dataframe(df)