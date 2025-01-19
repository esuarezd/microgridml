from pymodbus.client import ModbusTcpClient
from time import time
# Diccionario global para mantener conexiones persistentes
connections = {}

def get_or_create_connection(device):
    """Obtiene o crea una conexión persistente."""
    host = device['host']
    port = device['port']

    try:
        if host not in connections:
            client = ModbusTcpClient(host = host, port = port)
            if not client.connect():
                device['connection_status'] = "Failure"
                timestamp = time()
                print(f"{timestamp}: Advertencia. No se pudo conectar al equipo en {host}:{port}")
                return None
            
            device["connection_status"] = "Good"
            connections[host] = client
        return connections[host]
    except Exception as e:
        timestamp = time()
        print(f"{timestamp}: Error al intentar conectar con {host}:{port}: {e}")
        return None

def get_signals(device_id, device, signals):
    # device: list
    # mapping: list
    
    client = get_or_create_connection(device)

    if not client():
        device["connection_status"] = "Failure"
        timestamp = time()
        print(f"{timestamp}: Advertencia. No se pudo establecer la conexión para el dispositivo {device_id}") 
        return {}

    results = {}
    for signal in signals:
        try:
            address = signal["address"]
            slave = signal["slave"]
            result = client.read_input_registers(address = address, slave = slave)

            if result.isError():
                timestamp = time()
                print(f"{timestamp}: Advertencia. No se pudo leer la señal {signal.get('signal_id', 'signal_id no encontrado')} la dirección {address} con slave {slave} del dispositivo {device_id}")
            else:
                value = result.registers[0]
                results[signal["name"]] = value
        except Exception as e:
            timestamp = time()
            print(f"{timestamp}: Error al procesar la señal {signal.get('signal_id', 'signal_id no encontrado')} del dispositivo {device_id}: {e}")
    return results

def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    for client in connections.values():
        client.close()
    connections.clear()