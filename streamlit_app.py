import streamlit as st
import pandas as pd
import data_collect

# Cargar dispositivos IoT y protocolos
iot_devices = data_collect.get_iot_devices()

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
    index=0
)

if menu == "Home":
    st.title("Home - Datos de los Dispositivos IoT")
    st.write("Próximamente se mostrarán los datos leídos de los dispositivos.")

elif menu == "Comm":
    st.title("Comm - Estado de Comunicaciones")
    st.subheader("Estado de los Dispositivos IoT")
    # Encabezados de las columnas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Enabled**")
    with col2:
        st.markdown("**Device Name**")
    with col3:
        st.markdown("**IP Address**")
    with col4:
        st.markdown("**Protocol Name**")
    with col5:
        st.markdown("**Connection Status**")

    # Filas dinámicas para cada dispositivo
    for device in iot_devices:
        col1, col2, col3, col4, col5 = st.columns(5)

        # Casilla de habilitación sin duplicar texto
        with col1:
            was_enabled = device["enabled"]
            device["enabled"] = st.checkbox("", 
                                            value=device["enabled"], 
                                            key=f"enabled_{device['device_id']}"  # Clave única basada en el ID del dispositivo
                                            )

            # Si cambia el estado de "enabled", conecta o desconecta el dispositivo
            if device["enabled"] != was_enabled:
                if device["enabled"]:
                    data_collect.connect_device(device)  # Intenta conectar
                else:
                    device["connection_status"] = "Unknown"  # Desconexión

        with col2:
            st.write(device["device_name"])
        with col3:
            st.write(device["ip_address"])
        with col4:
            st.write(device["protocol_name"])
        with col5:
            status_color = (
                "green" if device["connection_status"] == "OK" else
                "red" if device["connection_status"] == "Failure" else
                "gray"
            )
            st.markdown(
                f"<span style='color: {status_color}; font-weight: bold;'>{device['connection_status']}</span>",
                unsafe_allow_html=True
            )

    # Refrescar periódicamente si es necesario
    st.button("Actualizar estado")  # Botón manual para actualizar
