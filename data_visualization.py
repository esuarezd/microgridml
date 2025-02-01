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
            "connection_status": device_info.get('value', None),
        }
        for device_info in device_data
    ]
    return device_list