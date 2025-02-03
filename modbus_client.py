from pymodbus.client import ModbusTcpClient
from datetime import datetime
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
        logging.FileHandler("logs/modbus_client.log", mode="a")
    ]
)

# Diccionario global para mantener conexiones persistentes
connections = {}

def get_or_create_connection(device):
    """Obtiene o crea una conexión persistente."""
    device_id = device.get('device_id', None)
    host = device.get('host', None)
    port = device.get('port', 502)
    
    try:
        if host not in connections or not connections[host].is_socket_open():
            client = ModbusTcpClient(host=host, port=port)
            if not client.connect():
                logging.warning(f"No se pudo conectar al equipo en {host}:{port}")
                return None
            
            connections[host] = client
        # fin if
        return connections[host]
    except Exception as e:
        logging.error(f"Error al intentar conectar con {host}:{port}: {e}")
        return None

def get_signals(device, device_signals):
    """Lee las señales de un dispositivo Modbus."""
    device_id = device.get('device_id', None)
    results = list()
    connection_status = {
        'device_id': device_id, 
        'value': None, 
        'timestamp': datetime.now().timestamp(), 
        'source': 1, 
        'quality': 1
    }

    client = get_or_create_connection(device)
    
    if not client or not client.is_socket_open():
        connection_status.update(
            {
                'value': 'Failure'   
            }
        )
        logging.warning(f"No se pudo establecer la conexión para el dispositivo {device_id}")
        return connection_status,

    
    connection_status.update(
        {
            'value': 'Connected'
        }
    )
    for signal in device_signals:
        try:
            if signal['enabled']:
                address = signal['address']
                slave = signal['slave_id']
                signal_id = signal.get('signal_id')
                result = client.read_input_registers(address=address, slave=slave)
                modbus_data = {
                    'signal_id': signal_id, 
                    'address': address, 
                    'slave': slave, 
                    'timestamp': datetime.now().timestamp()
                }
                if result.isError():
                    logging.warning(f"No se pudo leer la señal {signal.get('signal_id', 'signal_id no encontrado')} en la dirección {address} con slave {slave} del dispositivo {device_id}")
                else:  
                    if result.registers:
                        value_protocol = result.registers[0]
                        modbus_data.update(
                            {
                                'value_protocol': value_protocol,
                                'quality': 1,
                                'source': 1
                            }
                        )
                        results.append(modbus_data)
        except Exception as e:
            logging.error(f"Error al procesar la señal {signal.get('signal_id', 'signal_id no encontrado')} del dispositivo {device_id}: {e}")
    return connection_status, results

def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    for client in connections.values():
        client.close()
    connections.clear()
    logging.info("Todas las conexiones se han cerrado.")


