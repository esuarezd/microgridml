import pandas as pd
import streamlit as st
import threading
import logging
import time
import asyncio
# app local
import data_collector
import utils

# Cargar configuraciones
iot_devices = utils.load_json("config_iot_devices.json")
iot_protocols = utils.load_json("config_iot_protocols.json")
iot_signals = utils.load_json("config_iot_signals.json")

# preprocesar configuraciones
device_data = data_collector.preprocess_configuration_devices(iot_devices, iot_protocols, iot_signals)
realtime_data = data_collector.preprocess_configuration_signals(iot_devices, iot_signals)
# Iniciar hilos de recolección de datos para dispositivos habilitados
for device_id, device_info in device_data.items():
    if device_info["device"]["enabled"]:
        thread = threading.Thread(
            target=data_collector.host_data_collection,
            args=(device_id, device_info["device"], device_info["signals"], realtime_data),
            daemon=True
        )
        thread.start()
        logging.info(f"Hilo iniciado para el dispositivo {device_id}: {device_info['device']['device_name']}")

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)


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
    placeholder = st.empty()

    async def update_table():
        while True:
            # Generar lista de señales
            signals_list = [
                {
                    "signal_id": signal_info["signal_id"],
                    "obj_path": signal_info["obj_path"],
                    "signal_name": signal_info["signal_name"],
                    "signal_type": signal_info["signal_type"],
                    "value": signal_info["value"],
                    "unit": signal_info["unit"],
                    "timestamp": signal_info["timestamp"],
                }
                for signal_info in realtime_data.values()
            ]
            df_rt = pd.DataFrame(signals_list)

            # Formatear timestamp si hay datos
            if not df_rt.empty:
                df_rt["timestamp"] = pd.to_datetime(df_rt["timestamp"], unit="s").dt.strftime("%Y-%m-%d %H:%M:%S")

            # Actualizar la tabla en el placeholder
            placeholder.dataframe(df_rt)

            # Esperar un segundo antes de actualizar
            await asyncio.sleep(20)

    # Iniciar la tarea asíncrona
    asyncio.run(update_table())


elif st.session_state["page"] == "History":
    st.title("Microgrid ML")
    st.write("Historial de lecturas de señales (en desarrollo).")

elif st.session_state["page"] == "Devices":
    st.title("Microgrid ML")
    st.write("Estado comunicación de los Dispositivos IoT. version 19-Ene 8:43 pm")

    # Construir DataFrame para dispositivos
    device_list = [
        {
            "enabled": device_info["device"]["enabled"],
            "device_id": device_info["device"]["device_id"],
            "device_name": device_info["device"]["device_name"],
            "host": device_info["device"]["host"],
            "protocol_name": device_info["device"]["protocol_name"],
            "connection_status": device_info["device"]["connection_status"],
        }
        for device_info in device_data.values()
    ]
    df_devices = pd.DataFrame(device_list)
    if df_devices.empty:
        st.write("No hay dispositivos configurados.")
    else:
        st.dataframe(df_devices)

# Manejo de cierre de conexiones
#st.sidebar.button("Cerrar conexiones", on_click=data_collector.close_all_connections)
