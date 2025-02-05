import multiprocessing
import json
import time
import logging
import os
from multiprocessing.managers import BaseManager

#local import
import app.modbus_client as modbus_client

# Verificar si la carpeta 'logs' existe, si no, crearla
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler("logs/data_collector.log", mode="a")  # Registrar en un archivo
    ]
)


    
def build_configuration_devices(iot_devices, iot_protocols, group_name):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    device_data = list()

    for device in iot_devices:
        protocol_id = device["protocol_id"]

        protocol_name = next((m["protocol_name"] for m in iot_protocols if m["protocol_id"] == protocol_id), "Unknown")

        device_data.append( 
            { 
            **device, 
            "protocol_name": protocol_name, 
            "group_name": group_name,
            "value": 0,
            "quality": 0,
            "source": 0,
            "timestamp": 0
            }
        )
    #logging.info(f"Device data preprocessed: {device_data}")
    return device_data

def build_configuration_signals(iot_signals, group_id, group_name):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    signals_data = list()

    for iot_signal in iot_signals:
        device_signals = iot_signal["device_signals"]
        for signal in device_signals:
            if signal["group_id"] == group_id:

                signals_data.append( 
                    { 
                    **signal, 
                    'group_name': group_name,
                    'value_protocol': 0,
                    'value': 0,
                    'quality': 0,
                    'source': 0,
                    'timestamp': 0
                    }
                )
    #logging.info(f"Signals data preprocessed: {signals_data}")
    return signals_data    

def host_data_collection(realtime_data, device, device_signals):
    """Hilo de recolección de datos para un dispositivo específico.

    Args:
        device (dict): diccionario con los datos del equipo
        device_signals (dict): diccionario con las señales que se leen del equipo
        realtime_data (dic): dicctionario con los datos de tiempo real del sistema
    """
    device_id = device.get("device_id")
    protocol_id = device.get("protocol_id")
    if protocol_id == 0: # ModbusTcpClient
            logging.info(f"start connection to device {device_id}")
            modbus_client.main(realtime_data, device, device_signals)
    elif protocol_id == 1: # Mqtt
        pass
    elif protocol_id == 2: # dds
        pass
    else:
        logging.warning(f"Unknown protocol_id {protocol_id} for device {device_id}")

            

def build_realtime_data(realtime_data, iot_devices, iot_protocols, iot_signals, signals_group):
    """constructor del diccionario realtime_data

    Args:
        iot_devices (list): lista de equipos
        iot_protocols (list): lista de protocolos
        iot_signals (list): listado de señales por equipo
        signals_group (list): grupo de señalziacion en el sistema
        realtime_data (dict): diciconario con las señales organizado segun signals_group
    """
    # preprocesar configuraciones
    for group in signals_group:
        group_id = group.get('group_id')
        group_name = group.get('group_name')
        if group_id == 0:
            realtime_data[group_id] = build_configuration_devices(iot_devices, iot_protocols, group_name)
            logging.info(f"Device configuration loaded")
        else:
            realtime_data[group_id] = build_configuration_signals(iot_signals, group_id, group_name)
            logging.info(f"Signals configuration loaded for group {group_id}")
    #return realtime_data

def load_json(file_path):
    """Carga un archivo JSON con manejo de excepciones."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: El archivo {file_path} no tiene un formato JSON válido. Detalles: {e}")
        return None



def delete_start_data_collection(iot_devices, iot_signals, realtime_data):
    
    # Iniciar hilos de recolección de datos para dispositivos habilitados
    
    for device in iot_devices:
        if device["enabled"]:
            device_signals = next((m["device_signals"] for m in iot_signals if m["device_id"] == device["device_id"]), "Unknown")

            process = multiprocessing.Process(
                target=host_data_collection,
                args=(device, device_signals, realtime_data),
                daemon=True
            )
            process.start()
            process.join()
            logging.info(f"Proceso iniciado para el dispositivo {device['device_id']}: {device['device_name']}")

# Definir la clase para manejar el diccionario compartido
class RealtimeDataManager(BaseManager):
    pass

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    realtime_data = manager.dict()

    # Registrar el diccionario para que pueda ser accedido por otros procesos (como Streamlit)
    RealtimeDataManager.register('get_realtime_data', callable=lambda: realtime_data)

    # Iniciar el servidor que expondrá los datos
    server = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
    server.start()
    try:
        logging.info(f"Backend ejecutándose en 127.0.0.1:50000...")

        # Cargar configuraciones
        iot_devices = load_json("data/config_iot_devices.json")
        iot_protocols = load_json("data/config_iot_protocols.json")
        iot_signals = load_json("data/config_iot_signals.json")
        signals_group = load_json("data/config_signals_group.json")

        #build_realtime_data(realtime_data, iot_devices, iot_protocols, iot_signals, signals_group)

        # Iniciar la recolección de datos
        #start_data_collection(iot_devices, iot_signals, realtime_data)
        for device in iot_devices:
            if device["enabled"]:
                device_signals = next((m["device_signals"] for m in iot_signals if m["device_id"] == device["device_id"]), ["Unknown"])

                process = multiprocessing.Process(
                    target=host_data_collection,
                    args=(realtime_data, device, device_signals)
                )
                process.start()
                logging.info(f"Proceso iniciado para el dispositivo {device['device_id']}: {device['device_name']}")

        # Mantener el backend activo
        logging.info(f"Backend ejecutándose...")
        while True:
            time.sleep(1)
    except Exception as e:
        logging.error(f"Unexpected error for BaseManager: {e}")
        logging.info("Shutting down server ...")
        server.shutdown()