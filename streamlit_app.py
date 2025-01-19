import streamlit as st
import data_collector
import utils

# Cargar configuraciones
iot_protocols = utils.load_json("config_iot_protocols.json")
iot_devices = utils.load_json("config_iot_devices.json")
iot_signals = utils.load_json("config_iot_signals.json")

# agregamos llave protocol_name en iot_devices
for device in iot_devices:
    device['protocol_name'] = data_collector.get_protocol_name(device['protocol_id'], iot_protocols)

# creacion de nuestr
data_devices = data_collector.preprocess_configuration(iot_devices, iot_signals)


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
        st.markdown("**host**")
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
            st.write(device["host"])
        with col5:
            protocol_name = data_collector.get_protocol_name(device['protocol_id'], iot_protocols)
            st.write(protocol_name)

        # Mostrar el estado de la conexión
        with col6:
            status_color = (
                "green" if  device["connection_status"] == "Good" else
                "red" if device["connection_status"] == "Failure" else "gray"
            )
            st.markdown(
                f"<span style='color: {status_color};'>{device['connection_status']}</span>",
                unsafe_allow_html=True
            )

