import json
from pymodbus.client import ModbusTcpClient

# Cargar datos desde un archivo JSON
def get_json(path):
    with open(path, "r") as file:
        return json.load(file)

def get_iot_devices():
    iot_devices = get_json("iot_devices.json")
    protocols = get_json("protocols.json")
    for device in iot_devices:
        # Añadir el nombre del protocolo si no existe
        device["protocol_name"] = get_protocol_name(device["protocol_id"], protocols)
    return iot_devices

# Obtener el nombre del protocolo
def get_protocol_name(protocol_id, protocols):
    for protocol in protocols:
        if protocol["protocol_id"] == protocol_id:
            return protocol["protocol_name"]
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

