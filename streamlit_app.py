import streamlit as st
import pandas as pd
import data_collect

# Cargar dispositivos IoT y protocolos
iot_devices = data_collect.get_iot_devices()
iot_mapping = data_collect.get_iot_mapping()

for i in range(len(iot_devices)):
    if (iot_devices[i]["enabled"]):
        data_collect.connect_device(iot_devices[i], iot_mapping[i]["mapping"])

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

if st.sidebar.button("History"):
    st.session_state["page"] = "History"

if st.sidebar.button("Devices"):
    st.session_state["page"] = "Devices"

#if menu == "Home":
if st.session_state["page"] == "Home":
    st.title("Microgrid ML")
    st.write("Sistema IoT")
    st.write(f"{iot_mapping[0]['mapping'][1]['name']}: {iot_mapping[0]['mapping'][1]['value']}")

#elif menu == "His":
elif st.session_state["page"] == "History":
    st.title("Microgrid ML")
    st.write("Historial")

#elif menu == "Comm":
elif st.session_state["page"] == "Devices":
    st.title("Microgrid ML")
    st.subheader("Estado comunicacion de los Dispositivos IoT")
    # Encabezados de las columnas
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown("**enabled**")
    with col2:
        st.markdown("**device_id**")
    with col3:
        st.markdown("**device_name**")
    with col4:
        st.markdown("**ip_address**")
    with col5:
        st.markdown("**protocol_name**")
    with col6:
        st.markdown("**connection_status**")

    # Filas dinámicas para cada dispositivo
    for device in iot_devices:
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        # Mostrar datos del dispositivo
        with col1:
            st.write(device["enabled"])
        with col2:
            st.write(device["device_id"])
        with col3:
            st.write(device["device_name"])
        with col4:
            st.write(device["ip_address"])
        with col5:
            st.write(device["protocol_name"])

        # Mostrar el estado de la conexión
        with col6:
            status_color = (
                "green" if  device["connection_status"] == "OK" else
                "red" if device["connection_status"] == "Failure" else "gray"
            )
            st.markdown(
                f"<span style='color: {status_color};'>{device['connection_status']}</span>",
                unsafe_allow_html=True
            )

