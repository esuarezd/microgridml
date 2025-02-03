import logging
import time
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

def update_realtime_data(signals_group, modbus_node, device_id, signal_id):

    for signal in signals_group:
        if signal_id == modbus_node.get('signal_id'):
            # read scale factor and offset from attrubites of configuration
            scale_factor = signal.get('scale_factor', 1)
            offset = signal.get('offset', 0)
            data_type = signal.get('data_type')
            # read the value read via protocol and create new value
            value_protocol = modbus_node.get('value')
            if data_type == "uint16":
                # Convertir el valor a un número uint16
                value_data_type = value_protocol & 0xFFFF
            elif data_type == "int16" and (modbus_node.get('value') > 32767):
                value_data_type = value_protocol - 65536
            else: # int16
                value_data_type = value_protocol
            value = offset + (value_data_type / scale_factor)
            signal.update(
                {
                    'value_protocol': value_protocol,
                    'value_data_type': value_data_type,
                    'value':value,
                    'timestamp':modbus_node.get('timestamp'),
                    'quality':modbus_node.get('quality'),
                    'source':modbus_node.get('source')
                }
            )
            logging.info(f"Datos actualizados: device_id:{device_id}, signal_id: {signal_id}, name:{signal.get('signal_name')}, data type: {signal.get('data_type')}, value protocol:{signal.get('value_protocol')}, scale factor: {signal.get('scale_factor')}, value: {signal.get('value')}, timestamp: {signal.get('timestamp')}")
            break 
    return signals_group

def new_modbus_node(signal_id):
    modbus_node = {
        'signal_id': signal_id, 
        'value': 0,
        'timestamp': datetime.now().timestamp(),
        'quality':0,
        'source':0
    }
    return modbus_node

def main(device, device_signals, realtime_data):
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
            contador = 0
            for signal in device_signals:
                enabled = signal.get('enabled')
                if enabled:    
                    function_code = signal.get('function_code', 4)
                    address = signal.get('address')
                    signal_id = signal.get('signal_id')
                    group_id = signal.get('group_id')
                    modbus_node = new_modbus_node(signal_id)
                    if function_code == 1:
                        pass
                    elif function_code == 2:
                        pass
                    elif function_code == 4:
                        modbus_input_register = client.read_input_registers(reg_addr=address)
                        if modbus_input_register:
                            value = modbus_input_register[0]
                            modbus_node.update({'value': value, 'quality': 1, 'source': 1})
                            pos = get_pos(realtime_data[group_id], signal_id)
                            realtime_data[group_id][pos] = update_element(realtime_data[group_id], modbus_node, device_id, signal_id)
                    else:
                        logging.warning(f"No hay function code definido para la señal con signal_id {signal.get('signal_id')}")
                    time.sleep(2)
                    contador += 1
            time.sleep(interval - contador*2)
    
    except ConnectionError as ce:
        logging.error(f"Connection lost for device {device_id}: {ce}")
        client.close()

    except Exception as e:
        logging.error(f"Unexpected error for device {device_id}: {e}")
        client.close()
