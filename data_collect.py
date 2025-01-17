import json
import modbus_client

# Cargar datos desde un archivo JSON
def get_json(path):
    with open(path, "r") as file:
        return json.load(file)

# Crear un diccionario de búsqueda para protocolos
def build_protocol_lookup(protocols):
    return {protocol["protocol_id"]: protocol["protocol_name"] for protocol in protocols}

# Obtener dispositivos IoT con el nombre del protocolo agregado
def get_iot_devices():
    iot_devices = get_json("iot_devices.json")
    protocols = get_json("protocols.json")
    protocol_lookup = build_protocol_lookup(protocols)  # Crear diccionario de búsqueda
    # el dict seria asi protocol_lookup = { 0: "ModbusTcpClient",1: "Mqtt"}
    for device in iot_devices:
        # Asignar el nombre del protocolo desde el diccionario de búsqueda
        device["protocol_name"] = protocol_lookup.get(device["protocol_id"], "Unknown Protocol")
    
    return iot_devices

def get_iot_mapping():
    iot_mapping = get_json("iot_mapping.json")
    return iot_mapping

# Conectar al dispositivo IoT
def connect_device(device, mapping):
    
    match device["protocol_id"]:
        case 0: #ModbusTcpClient
            data_device = modbus_client.connect_device(device, mapping)
        case 1: #mqtt
            pass
    
    return data_device

def get_data_from_iot_device(iot_device):
    pass