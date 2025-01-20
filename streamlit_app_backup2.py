# Interfaz de usuario
st.title("Aplicación de Lectura de Señales - Modbus TCP")

# Mostrar configuraciones cargadas
try:
    st.sidebar.write("Configuración de protocolos cargada:")
    st.sidebar.json(iot_protocols)
    st.sidebar.write("Configuración de dispositivos cargada:")
    st.sidebar.json(iot_devices)
    st.sidebar.write("Mapeo de señales cargado:")
    st.sidebar.json(iot_signals)
    st.sidebar.success("Recolección de datos en ejecución.")
except Exception as e:
    st.sidebar.error(f"Error al mostrar configuraciones: {e}")

# Manejo de cierre de conexiones
st.sidebar.button("Cerrar conexiones", on_click=data_collector.close_all_connections)