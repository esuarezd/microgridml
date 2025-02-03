import pandas as pd
import streamlit as st
import logging
import time
import os
from multiprocessing.managers import BaseManager

# local
import data_visualization

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
        return manager.get_realtime_data()
    except Exception as e:
        logging.error(f"Error conectando a datos en tiempo real: {e}")
        return None


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
    realtime_data = {}

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

if st.session_state["page"] == "Realtime":
    st.title("Microgrid ML")
    st.write("Datos de tiempo real. version 1-feb-2025 7:45 pm")
    placeholder = st.empty()  # Reservar espacio para la tabla de señales

    while True:
        if realtime_data:
            # Construcción de la tabla de tiempo real
            data_list = []
            for group_id, signals in realtime_data.items():
                if group_id != 0:  # Excluir dispositivos, solo mostrar señales
                    for signal in signals:
                        data_list.append({
                            "enable":signal.get("enabled"),
                            "group_name":signal.get("group_name"),
                            "path1":signal.get("path1"),
                            "Signal Name": signal.get("signal_name"),
                            "Value": signal.get("value"),
                            "Last Updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(signal.get("timestamp", 0)))
                        })
            df = pd.DataFrame(data_list)
            placeholder.dataframe(df)
        else:
            placeholder.error("No se pudo conectar al backend de datos en tiempo real.")

        time.sleep(60)  # Refrescar cada 5 segundos
    


elif st.session_state["page"] == "History":
    st.title("Microgrid ML")
    st.write("Historial de lecturas de señales (en desarrollo).")

elif st.session_state["page"] == "Devices":
    st.title("Microgrid ML")
    st.write("Estado comunicación de los Dispositivos IoT (Versión 1-Feb 9:23 pm)")

    device_placeholder = st.empty()  # Reservar espacio para la tabla de dispositivos

    while True:
        if realtime_data:
            devices = realtime_data.get(0, [])  # group_id = 0 para dispositivos
            device_list = [
                {
                    "enabled": device.get("enabled"),
                    "Device ID": device.get("device_id"),
                    "Device Name": device.get("device_name"),
                    "Host": device.get("host"),
                    "Protocol": device.get("protocol_name"),
                    "Status": device.get("value", None),  # Este campo muestra "Good", "Failure", etc.
                    "Last Updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(device.get("timestamp", 0)))
                }
                for device in devices
            ]

            df_devices = pd.DataFrame(device_list)
            device_placeholder.dataframe(df_devices)
        else:
            device_placeholder.error("No hay información de dispositivos disponible.")

        time.sleep(60)  # Refrescar cada 5 segundos
