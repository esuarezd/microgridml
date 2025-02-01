import pandas as pd
import streamlit as st
import logging
from multiprocessing.managers import BaseManager
import os

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
    manager = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
    manager.connect()
    return manager.get_realtime_data()


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
    st.write("Datos de tiempo real. version 21-Ene 1:00 am")
    st.write("Paneles Solares:")
    # Placeholder para la tabla
    


elif st.session_state["page"] == "History":
    st.title("Microgrid ML")
    st.write("Historial de lecturas de señales (en desarrollo).")

elif st.session_state["page"] == "Devices":
    st.title("Microgrid ML")
    st.write("Estado comunicación de los Dispositivos IoT (Versión 1-Feb 2:11 pm)")

    # Construir DataFrame para dispositivos
    group_id=0
    device_data = realtime_data.get(group_id, None)
    if device_data is None:
        st.write("No hay dispositivos configurados.")
    else:
        device_list = data_visualization.get_device_list(device_data)
        df_devices = pd.DataFrame(device_list)
        st.dataframe(df_devices)

# Manejo de cierre de conexiones
#st.sidebar.button("Cerrar conexiones", on_click=data_collector.close_all_connections)
