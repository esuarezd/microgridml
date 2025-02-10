import logging
import time
import json
from pyModbusTCP.client import ModbusClient
from datetime import datetime

# Definir la ruta del directorio de logs 
log_file = 'logs/collection/modbus.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

def new_modbus_node():
    """_summary_

    Returns:
        dict: nodo modbus
    """
    modbus_node = {
        'value_protocol': 0,
        'timestamp': 0,
        'quality':0,
        'source':0
    }
    return modbus_node

def scale_value(signal,modbus_node):
    scale_factor = signal.get('scale_factor', 1)
    offset = signal.get('offset', 0)
    data_type = signal.get('data_type')
    value_protocol = modbus_node.get('value_protocol')
    
    if data_type == "uint16":
        # Convertir el valor a un número uint16
        value_data_type = value_protocol & 0xFFFF
    elif data_type == "int16" and (modbus_node.get('value_protocol') > 32767):
        value_data_type = value_protocol - 65536
    else: # int16
        value_data_type = value_protocol
    
    value = offset + (value_data_type / scale_factor)
    return value
    
def update_realtime_data(realtime_data, signal, modbus_node, value, groups_dict):
    """_summary_

    Args:
        realtime_data (Proxy List): lista de las señales de tiempo real
        device_id (int): id del equipo
        signal (dict): datos de la señal del sensor
        modbus_node (dict): datos de lectura via modbus asociado a signal
    """
    realtime_signal_value = {
        **signal, # Copiar todos los elementos de signals
        **modbus_node, # Copiar todos los elementos de modbus_node
        "value": value,
    }
    signal_id = signal.get('signal_id')
    if signal_id not in realtime_data:  # Si la señal no existe en el diccionario
        # Agregar la nueva señal con su valor
        realtime_data[signal_id] = realtime_signal_value
    elif realtime_data[signal_id].get('value') != value:  # Si el valor actual es diferente
        # Actualizar el valor de la señal
        realtime_data[signal_id] = realtime_signal_value


def save_dictproxy_to_json(realtime_data, file_path='data/realtime_data_DictProxy.json'):
    """Guarda el diccionario realtime_data en un archivo JSON para depuración."""
    try:
        # Convertir el diccionario compartido a uno normal antes de guardar
        data_to_save = {k: v for k, v in realtime_data.items()}
        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        logging.info(f"modbus: realtime_data guardado exitosamente en {file_path}")
    except Exception as e:
        logging.error(f"modbus: Error al guardar realtime_data en JSON: {e}")

def client(realtime_data, device, device_signals, groups_dict):
    """ Cliente tcp Modbus

    Args:
        device (dict): datos de conexion al equipo
        device_signals (list): listado de señales del equipo
        realtime_data (Proxy List): los datos de tiempo real del sistema
    """
    try:
        device_id = device.get('device_id')
        interval = device.get('interval', 60)
        host = device.get('host')
        port = device.get('port',502)
        unit_id = device.get('unit_id', 1)
        client = ModbusClient(host=host,port=port,unit_id=unit_id)
        client.open()
        logging.info(f"modbus: Device {device_id} is open...")
        while True:
            for signal in device_signals:
                enabled = signal.get('enabled')
                if enabled:
                    signal_id = signal.get('signal_id')  
                    function_code = signal.get('function_code', 4)
                    address = signal.get('address')
                    modbus_node = new_modbus_node()
                    modbus_node['timestamp'] = datetime.now().timestamp()
                    if function_code == 1:
                        pass
                    elif function_code == 2:
                        pass
                    elif function_code == 4:
                        modbus_input_register = client.read_input_registers(reg_addr=address)
                        if modbus_input_register:
                            value_protocol = modbus_input_register[0]
                            modbus_node["value_protocol"] = value_protocol 
                            modbus_node["source"] = 1   #para quality nos toca leer otro registro
                            logging.info(f"modbus: Datos de device: {device_id}, signal_id: {signal_id}, modbus: {modbus_node}")
                            value = scale_value(signal,modbus_node)
                            update_realtime_data(realtime_data, signal, modbus_node, value, groups_dict)
                            #save_dictproxy_to_json(realtime_data)
                    else:
                        logging.warning(f"modbus: No hay function code definido para la señal con signal_id {signal.get('signal_id')}")
            time.sleep(interval)
    
    except ConnectionError as ce:
        logging.error(f"modbus: Connection lost for device {device_id}: {ce}")
        client.close()

    except Exception as e:
        logging.error(f"modbus: Unexpected error for device {device_id}: {e}")
        client.close()
