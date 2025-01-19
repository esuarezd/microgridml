from pymodbus.client import ModbusTcpClient
from time import sleep, time
# Diccionario global para mantener conexiones persistentes
connections = {}

def get_or_create_connection(host, port):
    """Obtiene o crea una conexión persistente."""
    if host not in connections:
        client = ModbusTcpClient(host, port)
        if not client.connect():
            raise ConnectionError(f"No se pudo conectar al equipo en {host}:{port}")
        connections[host] = client
    return connections[host]

def get_signals(device, mapping):
    # device: list
    # mapping: list
    
    results = {}
    if not device["enabled"]:
         device["connection_status"] = "Unknown"
    else:
        client = get_or_create_connection(device["host"], device["port"])
        if client.connect():
            device["connection_status"] = "Good"
            device_id = device["device_id"]
            results = {}

            for signal in mapping:
                address = signal["address"]
                slave = signal["slave"]
                match signal["function_code"]:
                    case "01":
                        pass
                    case "04":
                        response = client.read_input_registers(address = address, slave = slave)
                
                if response.isError():
                    raise Exception(f"Error al leer la dirección {address} del dispositivo {device_id}")
                
                value = response.registers[0]
                results[signal["name"]] = value

        else:
            device["connection_status"] = "Failure"
    return results