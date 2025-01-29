from pymodbus.client import ModbusTcpClient
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("modbus_client.log", mode="a")
    ]
)

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
                logging.warning(f"No se pudo conectar al equipo en {host}:{port}")
                return None
            
            connections[host] = client
        # fin if
        device["connection_status"] = "Good"
        return connections[host]
    except Exception as e:
        logging.error(f"Error al intentar conectar con {host}:{port}: {e}")
        return None

def get_signals(device, device_signals):
    """Lee las señales de un dispositivo Modbus."""
    device_id = device["device_id"]
    client = get_or_create_connection(device)

    if not client or not client.is_socket_open():
        device["connection_status"] = "Failure"
        logging.warning(f"No se pudo establecer la conexión para el dispositivo {device_id}")
        return {}

    results = dict()
    for signal in device_signals:
        try:
            if signal['enabled']:
                address = signal['address']
                slave = signal['slave_id']
                result = client.read_input_registers(address=address, slave=slave)
                if result.isError():
                    logging.warning(f"No se pudo leer la señal {signal.get('signal_id', 'signal_id no encontrado')} en la dirección {address} con slave {slave} del dispositivo {device_id}")
                    results[signal["signal_id"]] = None  # Valor predeterminado en caso de error
                else:
                    signal_id = signal['signal_id']
                    scale_factor = signal.get('scale_factor', 1)
                    offset = signal.get('offset', 0)
                    if result.registers:
                        value_protocol = result.registers[0]
                        value_processed = (offset + value_protocol / scale_factor )
                        modbus_data = {
                        'value': value_processed,
                        'value_protocol': value_protocol,
                        'timestamp': datetime.now().timestamp(),
                        'quality': 1,
                        'source': 1
                        }
                    else:
                        modbus_data = {}
                    results[signal_id] = modbus_data
        except Exception as e:
            logging.error(f"Error al procesar la señal {signal.get('signal_id', 'signal_id no encontrado')} del dispositivo {device_id}: {e}")
            results[signal["signal_id"]] = None  # Valor predeterminado en caso de excepción
    return results

def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    for client in connections.values():
        client.close()
    connections.clear()
    logging.info("Todas las conexiones se han cerrado.")


