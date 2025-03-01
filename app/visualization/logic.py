import logging
import os
import time
from datetime import datetime
from multiprocessing.managers import BaseManager

#local import
from datastructure.list import array_list as array_list
from app.collection import model as model

# Definir la ruta del directorio de logs 
log_file = 'logs/visualization/logic.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

# Definir la clase para manejar el diccionario compartido
class RealtimeDataManager(BaseManager):
    pass

# Registrar el diccionario compartido
RealtimeDataManager.register('get_realtime_data')
    
data_dir = 'data'

def new_iot_system():
    # Creación del catalogo vacio
    app = {
        "devices": None,
        "protocols": None,
        "groups": None,
        "signals": None
    }

    # Inicialización de las estructuras de datos
    app["devices"] = array_list.new_list()
    app["protocols"] = array_list.new_list()
    app["groups"] = array_list.new_list()
    app["signals"] = array_list.new_list()

    return app

def load_iot_data(app, filename, key):
    data_file = os.path.join(data_dir, filename)
    app[key] = array_list.load_list(app[key], data_file)
    return array_list.size(app[key])

def load_data(app):
    load_iot_data(app, "config_iot/devices.json", "devices")
    load_iot_data(app, "config_iot/protocols.json", "protocols")
    load_iot_data(app, "config_iot/groups.json", "groups")
    load_iot_data(app, "config_iot/signals.json", "signals")
    logging.info(f"logic: Load IoT data successfully. {type(app)}")

def connect_to_realtime_data():
    try:
        manager = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
        manager.connect()
        logging.info("logic: Conectado al backend de datos en tiempo real.")
        manager_data = manager.get_realtime_data() # <class 'multiprocessing.managers.AutoProxy[get_realtime_data]'>
        # logging.info(f"logic: Leyendo multiprocess basemanager: {type(manager_data)}")
        realtime_data = manager_data.copy() #<class 'dict'>
        # logging.info(f"logic: nuevo tipo de dato de realtime: {type(realtime_data)}")
        return realtime_data
    except Exception as e:
        logging.error(f"logic: Error conectando a datos en tiempo real: {e}")
        return None
    
def build_devices_list(app):
    iot_devices = app["devices"]
    devices = iot_devices.get("elements")
    iot_protocols = app["protocols"]
    protocols = iot_protocols.get('elements')
    # Crear un diccionario de protocolos para mapear fácilmente
    protocol_dict = {protocol["protocol_id"]: protocol["protocol_name"] for protocol in protocols}

    # Extraer los datos que queremos y agregar el protocol_name
    output = []
    for device in devices:
        # Crear el nuevo diccionario con los campos deseados
        device_info = {
            "enabled": device["enabled"],
            "device_name": device["device_name"],
            "host": device["host"],
            "unit_id": device["unit_id"],
            "unit_name": device["unit_name"],
            "protocol_name": protocol_dict.get(device["protocol_id"], "Unknown")  # Buscar el nombre del protocolo
        }
        output.append(device_info)
    
    return output

def build_group_list(group_id, app, realtime_data):
    iot_groups = app["groups"]
    groups = iot_groups["elements"]
    group_dict = {group["group_id"]: group["group_name"] for group in groups}
    output = []
    for signal in realtime_data.values():
        if group_id == signal.get('group_id'):
            signal_type = signal.get('signal_type')
            
            # Para la hora local
            timestamp = signal.get('timestamp')
            local_datetime = datetime.fromtimestamp(timestamp)
            # Obtener la parte decimal del timestamp (microsegundos)
            microseconds = int((timestamp - int(timestamp)) * 1_000_000)
            
            signal_info = {
                "group_id": signal.get('group_id'),
                "group_name": group_dict.get(signal.get('group_id'), "Unknown"),
                "path1": signal.get('path1'),
                "path2": signal.get('path2', ''),
                "signal_id":signal.get('signal_id'),
                "singal_name": signal.get('signal_name'),
                "signal_type": "Analog" if signal_type else "Digital",
                # "value protocol": signal.get('value_protocol'),
                "value": signal.get('value'),
                "unit": signal.get('unit'),
                "timestamp": local_datetime.strftime('%Y-%m-%d %H:%M:%S') + f".{microseconds:06d}"
                #"timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(signal.get('timestamp')))
            }
            output.append(signal_info)
    return output

def read_analog_path1():
    data = model.read_sensor_path1(1)
    return data

def read_analog_path2(path1):
    data = model.read_sensor_path2(1, path1)
    return data

def read_analog_names(path1, path2):
    data = model.read_sensor_name(1, path1, path2)
    return data

def read_analog_signal_id(path1, path2, sensor_selected):
    data = model.read_sensor_signal_id(1, path1, path2, sensor_selected)
    return data

def read_analog_unit(path1, path2, sensor_selected):
    data = model.read_sensor_unit(1, path1, path2, sensor_selected)
    return data

def read_his_analog(signal_id, time_initial, time_final):
    data = model.read_his_analog(signal_id, time_initial, time_final)
    return data