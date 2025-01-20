from pymodbus.client import ModbusTcpClient
from datetime import datetime
import utils

# Diccionario global para mantener conexiones persistentes
connections = {}

def get_or_create_connection(device):
    """Obtiene o crea una conexión persistente."""
    host = device['host']
    port = device['port']

    try:
        if host not in connections or not connections[host].is_socket_open():
            client = ModbusTcpClient(host=host, port=port)
            if not client.connect():
                device['connection_status'] = "Failure"
                timestamp = utils.get_timestamp()
                print(f"{timestamp}: Advertencia. No se pudo conectar al equipo en {host}:{port}")
                return None
            
            connections[host] = client
        # fin if
        device["connection_status"] = "Good"
        return connections[host]
    except Exception as e:
        timestamp = utils.get_timestamp()
        print(f"{timestamp}: Error al intentar conectar con {host}:{port}: {e}")
        return None

def get_signals(device_id, device, signals):
    """Lee las señales de un dispositivo Modbus."""
    client = get_or_create_connection(device)

    if not client or not client.is_socket_open():
        device["connection_status"] = "Failure"
        timestamp = utils.get_timestamp()
        print(f"{timestamp}: Advertencia. No se pudo establecer la conexión para el dispositivo {device_id}")
        return {}

    results = {}
    for signal in signals:
        try:
            if signal["enabled"]:
                address = signal["address"]
                slave = signal["slave"]
                result = client.read_input_registers(address=address, slave=slave)
                timestamp = utils.get_timestamp()
                if result.isError():
                    print(f"{timestamp}: Advertencia. No se pudo leer la señal {signal.get('signal_id', 'signal_id no encontrado')} en la dirección {address} con slave {slave} del dispositivo {device_id}")
                    results[signal["signal_id"]] = None  # Valor predeterminado en caso de error
                else:
                    signal_id = signal["signal_id"]
                    value = result.registers[0]
                    data_modbus = {}
                    data_modbus['value'] = value
                    data_modbus['timestamp'] = datetime.now().timestamp() # Timestamp Unix con milisegundos. Ejemplo: 1672531199.123456
                    data_modbus['quality'] = 1
                    data_modbus['source'] = 1

                    results[signal_id] = data_modbus

                    #results[signal_id] = build_results(signal, value)
                    
        except Exception as e:
            timestamp = utils.get_timestamp()
            print(f"{timestamp}: Error al procesar la señal {signal.get('signal_id', 'signal_id no encontrado')} del dispositivo {device_id}: {e}")
            results[signal["name"]] = None  # Valor predeterminado en caso de excepción
    return results

def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    for client in connections.values():
        client.close()
    connections.clear()


