import logging
import time
import os
from pymodbus.client import ModbusTcpClient
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
        logging.FileHandler("logs/modbus.log", mode="a")  # Registrar en un archivo
    ]
)

def update_realtime_data(realtime_data, modbus_node):
    for signals_group in realtime_data.values():
        for signal in signals_group:
            signal_id = signal.get('signal_id')
            if signal_id == modbus_node.get('signal_id'):
                signal.update(
                    {
                        'value':modbus_node.get('value'),
                        'timestamp':modbus_node.get('timestamp'),
                        'quality':modbus_node.get('quality'),
                        'source':modbus_node.get('source')
                    }
                )
                return
    
def new_modbus_node(signal_id):
    modbus_node = {
        'signal_id': signal_id, 
        'value': 0,
        'timestamp': datetime.now().timestamp(),
        'quality':0,
        'source':0
    }
    return modbus_node

def client(device, device_signals, realtime_data):
    """ Cliente tcp Modbus

    Args:
        device (dict): datos de conexion al equipo
        device_signals (list): listado de señales del equipo
        realtime_data (dict): los datos de tiempo real del sistema
    """
    device_id = device.get('device_id')
    interval = device.get('interval', 60)
    host=device.get('host')
    port=device.get('port',502)
    client = ModbusTcpClient(host=host,port=port)
    try:
        client.open()
        logging.info(f"Client {device.get('device_name')} is online")
        while True:
            for signal in device_signals:
                function_code = signal.get('function_code', 4)
                address = signal.get('address')
                slave = signal.get('slave')
                signal_id = signal.get('signal_id')
                modbus_node = new_modbus_node(signal_id)
                if function_code == 1:
                    pass
                elif function_code == 2:
                    pass
                elif function_code == 4:
                    modbus_register = client.read_input_registers(address=address, slave=slave)
                    if modbus_register.registers:
                        value = modbus_register.registers[0]
                        modbus_node.update({'value': value, 'quality': 1, 'source': 1})
                else:
                    logging.warning(f"No hay function code definido para la señal con signal_id {signal.get('signal_id')}")
                update_realtime_data(realtime_data, modbus_node)
            time.sleep(interval)
    
    except ConnectionError as ce:
        logging.error(f"Connection lost for device {device_id}: {ce}")
        client.close()

    except Exception as e:
        logging.error(f"Unexpected error for device {device_id}: {e}")
