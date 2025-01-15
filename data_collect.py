import json
from pymodbus.client import ModbusTcpClient

# Cargar datos desde un archivo JSON
def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

# Buscar el nombre del protocolo según el protocolo_id
def get_protocol_name(protocol_id, protocols):
    for protocol in protocols:
        if protocol["protocolo_id"] == protocol_id:
            return protocol["protocolo_name"]
    return "Unknown Protocol"

# Conectar al dispositivo y leer datos
def connect_and_read(device):
    if device["protocol_id"] == 0:  # Modbus Tcp Client
        client = ModbusTcpClient(device["ip_address"])
        if client.connect():
            device["connection_status"] = "OK"
            # Aquí puedes agregar la lógica para leer datos del dispositivo.
        else:
            device["connection_status"] = "Failure"
    else:
        device["connection_status"] = "Protocol Not Supported"

# Actualizar el estado de los dispositivos
def update_device_status(devices, protocols):
    for device in devices:
        if device["enabled"]:
            connect_and_read(device)
        else:
            device["connection_status"] = "Unknown"
        device["protocol_name"] = get_protocol_name(device["protocol_id"], protocols)
    return devices
