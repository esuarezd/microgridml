import logging
import time
import json
import os
from pyModbusTCP.client import ModbusClient
from datetime import datetime

# Verificar si la carpeta 'logs' existe, si no, crearla
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler("logs/modbus_client.log", mode="a")  # Registrar en un archivo
    ]
)


def buscar_posicion(lista, llave, valor_buscado):
    for i, diccionario in enumerate(lista):
        if diccionario.get(llave) == valor_buscado:
            return i  # Devuelve la posición (índice) donde se encuentra el valor
    return -1  # Si no se encuentra el valor, retorna -1

def update_realtime_data(realtime_data, device_id, signal, modbus_node):
    signal_id = signal.get('signal_id')
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
    realtime_signal_value = {
        **modbus_node, 
        "value_data_type": value_data_type,
        "value": value,
        "group_id": signal.get('group_id'),
        "device_id": device_id
    }
    realtime_data.update(
        { 
            signal_id: realtime_signal_value
        }
    )


def new_modbus_node():
    modbus_node = {
        'value_protocol': 0,
        'timestamp': datetime.now().timestamp(),
        'quality':0,
        'source':0
    }
    return modbus_node

def save_realtime_data_to_json(realtime_data, file_path='data/realtime_data_snapshot.json'):
    """Guarda el diccionario realtime_data en un archivo JSON para depuración."""
    try:
        # Convertir el diccionario compartido a uno normal antes de guardar
        data_to_save = {k: v for k, v in realtime_data.items()}
        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        logging.info(f"realtime_data guardado exitosamente en {file_path}")
    except Exception as e:
        logging.error(f"Error al guardar realtime_data en JSON: {e}")


def main(realtime_data, device, device_signals):
    """ Cliente tcp Modbus

    Args:
        device (dict): datos de conexion al equipo
        device_signals (list): listado de señales del equipo
        realtime_data (dict): los datos de tiempo real del sistema
    """
    device_id = device.get('device_id')
    interval = device.get('interval', 60)
    host = device.get('host')
    port = device.get('port',502)
    unit_id = device.get('unit_id', 1)
    client = ModbusClient(host=host,port=port,unit_id=unit_id)
    try:
        client.open()
        logging.info(f"Device {device_id} is open...")
        while True:
            for signal in device_signals:
                enabled = signal.get('enabled')
                if enabled:
                    signal_id = signal.get('signal_id')  
                    function_code = signal.get('function_code', 4)
                    address = signal.get('address')
                    modbus_node = new_modbus_node()
                    if function_code == 1:
                        pass
                    elif function_code == 2:
                        pass
                    elif function_code == 4:
                        modbus_input_register = client.read_input_registers(reg_addr=address)
                        if modbus_input_register:
                            value = modbus_input_register[0]
                            modbus_node.update({"value_protocol": value, "quality": 1, "source": 1})
                            logging.info(f"Datos leidos de device_id:{device_id}, signal_id: {signal_id}, modbus: {modbus_node}")
                            update_realtime_data(realtime_data, device_id, signal, modbus_node)
                            #logging.info(f"Data updated de device_id:{device_id}, signal_id: {signal_id}, realtime_data: {realtime_data.get(signal_id)}")
                            #save_realtime_data_to_json(realtime_data)
                    else:
                        logging.warning(f"No hay function code definido para la señal con signal_id {signal.get('signal_id')}")
            time.sleep(interval)
    
    except ConnectionError as ce:
        logging.error(f"Connection lost for device {device_id}: {ce}")
        client.close()

    except Exception as e:
        logging.error(f"Unexpected error for device {device_id}: {e}")
        client.close()
