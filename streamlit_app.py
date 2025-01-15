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

# Menú de navegación
menu = st.sidebar.selectbox(
    "Menú",
    options=["Home", "Comm"],
    index=0  # Home como opción predeterminada
)

if menu == "Home":
    # Página principal - Datos leídos
    st.title("Home - Datos de los Dispositivos IoT")
    st.write("Próximamente se mostrarán los datos leídos de los dispositivos.")
    
elif menu == "Comm":
    # Página de comunicaciones
    st.title("Comm - Estado de Comunicaciones")
    st.subheader("Estado de los Dispositivos IoT")

    # Actualizar el estado de los dispositivos
    iot_devices = update_device_status(iot_devices, protocols)

    # Preparar datos para la tabla
    columns = ["Enabled", "Device Name", "IP Address", "Protocol Name", "Connection Status"]
    rows = [
        [
            device["enabled"],
            device["device_name"],
            device["ip_address"],
            device.get("protocol_name", "Unknown"),  # Obtener el nombre del protocolo
            device["connection_status"]
        ]
        for device in iot_devices
    ]

    # Crear DataFrame
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

    # Mostrar la tabla
    st.write(
        """
        La siguiente tabla muestra el estado de los dispositivos IoT. Puedes activar o desactivar la conexión y ver el resultado en la columna "Connection Status".
        """
    )
    st.dataframe(
        df.style.applymap(highlight_status, subset=["Connection Status"]),
        use_container_width=True
    )