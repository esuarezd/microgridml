import logging
import os
from multiprocessing.managers import BaseManager

#local import
from datastructure.list import array_list as array_list

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
    
