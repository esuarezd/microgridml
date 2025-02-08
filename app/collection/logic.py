import logging
import multiprocessing
import os
import sys
import time
from multiprocessing.managers import BaseManager

#local import
from app.collection import modbus as modbus
from datastructure.list import array_list as array_list

# Definir la ruta del directorio de logs 
log_file = 'logs/collection/logic.log'

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

def get_protocols_dict(app):
    protocols = app["protocols"]
    protocols_dict = {protocol["protocol_id"]: protocol["protocol_name"] for protocol in protocols["elements"]}
    return protocols_dict

def get_groups_dict(app):
    groups = app["groups"]
    groups_dict = {group["group_id"]: group["group_name"] for group in groups["elements"]}
    return groups_dict
    
def host_data_collection(realtime_data, device, device_signals, groups_dict):
    """Hilo de recolección de datos para un dispositivo específico.

    Args:
        device (dict): diccionario con los datos del equipo
        device_signals (dict): diccionario con las señales que se leen del equipo
        realtime_data (Proxy List): lista con los datos de tiempo real del sistema
    """
    device_id = device.get("device_id")
    protocol_id = device.get("protocol_id")
    if protocol_id == 0: # ModbusTcpClient
            logging.info(f"logic: start connection to device {device_id}")
            modbus.client(realtime_data, device, device_signals, groups_dict)
    elif protocol_id == 1: # Mqtt
        pass
    elif protocol_id == 2: # dds
        pass
    else:
        logging.warning(f"logic: Unknown protocol_id {protocol_id} for device {device_id}")

def start_data_collection(realtime_data, app):
    
    # Iniciar la recolección de datos
    groups_dict = get_groups_dict(app)
    protocols_dict = get_protocols_dict(app)
    iot_devices = app["devices"]
    iot_signals = app["signals"]
    
    for device in iot_devices["elements"]:
        if device["enabled"]:
            device_signals = next((m["device_signals"] for m in iot_signals["elements"] if m["device_id"] == device["device_id"]), ["Unknown"])

            process = multiprocessing.Process(
                target=host_data_collection,
                args=(realtime_data, device, device_signals, groups_dict), 
                daemon=True
            )
            process.start()
            logging.info(f"logic: Proceso iniciado para equipo {device['device_id']}: {device['device_name']}")
    while True: 
        time.sleep(10)

def main():
    try:
        # Cargar data de configiuracion
        # Se carga la configuracion iot para la aplicacion
        app = new_iot_system()
        load_data(app)
        
        # crear manager para multiproceso
        manager = multiprocessing.Manager()
        realtime_data = manager.dict()
        logging.info(f"logic: Objeto {type(realtime_data)} creado para realtime_data.")
        
        # Registrar el diccionario para que pueda ser accedido por otros procesos (como Streamlit)
        RealtimeDataManager.register('get_realtime_data', callable=lambda: realtime_data)
        logging.info("logic: Método 'get_realtime_data' registrado con éxito.")

        # Iniciar el servidor BaseManager
        server = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
        server.start()
        logging.info(f"logic: Backend ejecutándose en 127.0.0.1:50000...")

        start_data_collection(realtime_data, app)

    except KeyboardInterrupt:
        # Captura la interrupción de Ctrl+C para terminar el proceso de manera controlada
        logging.info("logic: Interrupción detectada (Ctrl+C), cerrando la aplicación.")
        server.shutdown()
        sys.exit(0)  # Termina el script de manera limpia
    except Exception as e:
        logging.error(f"logic: Unexpected error for BaseManager: {e}")
        logging.info("logic: Shutting down server ...")
        server.shutdown()
        sys.exit(1)  # Termina con un código de error