import streamlit as st
import pandas as pd
from data_collect import load_json, update_device_status

# Cargar dispositivos IoT y protocolos
iot_devices = load_json("iot_devices.json")
protocols = load_json("protocols.json")

# Configuración de la página
st.set_page_config(
    layout="wide",  
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)


st.title("Microgrid ML")
st.write("Sistema de comunicaciones")

# Actualizar el estado de los dispositivos
iot_devices = update_device_status(iot_devices, protocols)

# Preparar datos para la tabla
columns = ["Enabled", "Device id", "Device Name", "IP Address", "Protocol Name", "Connection Status"]
rows = [
    [
        device["enabled"],
        device["device_id"],
        device["device_name"],
        device["ip_address"],
        device["protocol_name"],
        device["connection_status"]
    ]
    for device in iot_devices
]

# Mostrar la tabla
st.subheader("Estado de los Dispositivos IoT")
st.write(
    """
    La siguiente tabla muestra el estado de los dispositivos IoT. Puedes activar o desactivar la conexión y ver el resultado en la columna "Connection Status".
    """
)

# Convertir a DataFrame para usar con Streamlit
df = pd.DataFrame(rows, columns=columns)

# Estilizar la columna "Connection Status"
def highlight_status(val):
    if val == "OK":
        return "background-color: green; color: white;"
    elif val == "Failure":
        return "background-color: red; color: white;"
    elif val == "Unknown":
        return "background-color: gray; color: white;"
    return ""

st.dataframe(
    df.style.applymap(highlight_status, subset=["Connection Status"]),
    use_container_width=True
)
