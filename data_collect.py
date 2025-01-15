import json
from pymodbus.client import ModbusTcpClient

# Cargar datos desde un archivo JSON
def load_json(path):
    with open(path, "r") as file:
        return json.load(file)

# Obtener el nombre del protocolo
def get_protocol_name(protocol_id, protocols):
    for protocol in protocols:
        if protocol["protocolo_id"] == protocol_id:
            return protocol["protocolo_name"]
    return "Unknown Protocol"

# Conectar al dispositivo IoT
def connect_device(device):
    if device["protocol_id"] == 0:  # Modbus Tcp Client
        client = ModbusTcpClient(device["ip_address"])
        if client.connect():
            device["connection_status"] = "OK"
        else:
            device["connection_status"] = "Failure"
    else:
        device["connection_status"] = "Protocol Not Supported"

# Actualizar dispositivos
def update_devices_status(devices, protocols):
    for device in devices:
        # Añadir el nombre del protocolo si no existe
        if "protocol_name" not in device:
            device["protocol_name"] = get_protocol_name(device["protocol_id"], protocols)

        # Si está habilitado, conecta al dispositivo
        if device["enabled"]:
            connect_device(device)
        else:
            device["connection_status"] = "Unknown"
