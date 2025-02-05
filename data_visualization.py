import logging
import os

# Verificar si la carpeta 'logs' existe, si no, crearla
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/data_visualization.log", mode="a")
    ]
)

def get_device_list(device_data):
    # Constructor de lista de equipos con su estado
    device_list = [
        {
            "enabled": device_info.get('enabled', None),
            "device_id": device_info.get('device_id', None),
            "device_name": device_info.get('device_name', None),
            "host": device_info.get('host', None),
            "protocol_name": device_info.get('protocol_name', None),
            "connection_status": device_info.get('value')
        }
        for device_info in device_data
    ]
    return device_list



"""
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
                    "unit id": device.get('unit_id'),
                    "Status": device.get("value", None),  # Este campo muestra "Good", "Failure", etc.
                    "Last Updated": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(device.get("timestamp", 0)))
                }
                for device in devices
            ]

            df_devices = pd.DataFrame(device_list)
            device_placeholder.dataframe(df_devices)
        else:
            device_placeholder.error("No hay información de dispositivos disponible.")

        time.sleep(60)
        """