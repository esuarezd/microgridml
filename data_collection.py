import multiprocessing
import json
import time
import logging
import os
from multiprocessing.managers import BaseManager

#local
import modbus_client

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


    
def preprocess_configuration_devices(iot_devices, iot_protocols, group_name):
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
            "value": None,
            "quality": 0,
            "source": 0,
            "timestamp": 0
            }
        )
    logging.info(f"Device data preprocessed: {device_data}")
    return device_data

def preprocess_configuration_signals(iot_signals, group_id, group_name):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    signals_data = list()

    for iot_signal in iot_signals:
        device_signals = iot_signal["device_signals"]
        for signal in device_signals:
            if signal["group_id"] == group_id:

                signals_data.append( 
                    { 
                    **signal, 
                    "group_name": group_name,
                    "value": 0,
                    "quality": 0,
                    "source": 0,
                    "timestamp": 0
                    }
                )
    logging.info(f"Signals data preprocessed: {signals_data}")
    return signals_data

def update_realtime_data(connection_status, results, signals_group, realtime_device_index, realtime_signal_index):
    """Actualiza datos leídos y el estado de conexión del dispositivo.

    Args:
        results (list): Datos que se leen del equipo.
        shared_realtime_data (dict): Datos en tiempo real.
        group_id (int): ID del grupo para las señales.
        device_status (dict, opcional): Estado de conexión del dispositivo.
    """
    for group in signals_group:
        group_id = group["group_id"]
        if group_id == 0:
            device_id = connection_status.get('device_id')
            if device_id in realtime_device_index:
                realtime_device_index[device_id].update(
                    {
                        'value':connection_status.get('value', None),
                        'timestamp':connection_status.get('timestamp', 0),
                        'source':connection_status.get('source',0),
                        'quality':connection_status.get('source',0)
                    }
                )
        else:
            for result in results:
                signal_id = result.get('signal_id')
                if signal_id in realtime_signal_index:
                    realtime_signal_index[signal_id].update({
                        'value': result.get('value', 0),
                        'value_protocol': result.get('value_protocol', 0),
                        'timestamp': result.get('timestamp', 0),
                        'quality': result.get('quality', 0),
                        'source': result.get('source', 0)
                    })
                else:
                    logging.warning(f"Signal ID {signal_id} not found in indexed data.")
    
    

def host_data_collection(device, device_signals, signals_group, realtime_device_index, realtime_signal_index):
    """Hilo de recolección de datos para un dispositivo específico.

    Args:
        device (dict): diccionario con los datos del equipo
        device_signals (dict): diccionario con las señales que se leen del equipo
        shared_realtime_data (dic): dicctionario con los datos de tiempo real del sistema
    """
    device_id = device["device_id"]
    protocol_id = device["protocol_id"]
    interval = device["interval"]
    while True:
        try:
            if protocol_id == 0:  # ModbusTcpClient
                connection_status, results = modbus_client.get_signals(device, device_signals)
                logging.info(f"Device {device_id} (protocol {protocol_id}) data collected: {results}")
                update_realtime_data(connection_status, results, signals_group, realtime_device_index, realtime_signal_index)
            elif protocol_id == 1:  # MQTT
                pass  # Implementación futura para MQTT
            elif protocol_id == 2:  # DDS
                pass  # Implementación futura para DDS
            else:
                logging.warning(f"Unknown protocol_id {protocol_id} for device {device_id}")

        except ConnectionError as ce:
            logging.error(f"Connection lost for device {device_id}: {ce}")
            device.update({"value":"Disconnected"})

        except Exception as e:
            logging.error(f"Unexpected error for device {device_id}: {e}")

        finally:
            time.sleep(interval)


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

def start_data_collection(shared_realtime_data):
    """Inicia la recolección de datos."""
    # Cargar configuraciones
    iot_devices = load_json("data/config_iot_devices.json")
    iot_protocols = load_json("data/config_iot_protocols.json")
    iot_signals = load_json("data/config_iot_signals.json")
    signals_group = load_json("data/config_signals_group.json")

    # preprocesar configuraciones
    for group in signals_group:
        group_id = group["group_id"]
        group_name = group["group_name"]
        if group_id == 0:
            shared_realtime_data[group_id] = preprocess_configuration_devices(iot_devices, iot_protocols, group_name)
            realtime_device_index = {device['device_id']: device for device in shared_realtime_data[group_id]}
            logging.info(f"Device data realtime: {realtime_device_index}")
        else:
            shared_realtime_data[group_id] = preprocess_configuration_signals(iot_signals, group_id, group_name)
            realtime_signal_index = {signal['signal_id']: signal for signal in shared_realtime_data[group_id]}
            logging.info(f"Signals data realtime: {realtime_signal_index}")

    # Iniciar hilos de recolección de datos para dispositivos habilitados
    
    for device in iot_devices:
        if device["enabled"]:
            device_signals = next((m["device_signals"] for m in iot_signals if m["device_id"] == device["device_id"]), "Unknown")

            multiprocessing.Process(
                target=host_data_collection,
                args=(device, device_signals, signals_group, realtime_device_index, realtime_signal_index),
                daemon=True
            ).start()
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

    logging.info("Backend ejecutándose en 127.0.0.1:50000...")

    # Iniciar la recolección de datos
    start_data_collection(realtime_data)

    # Mantener el backend activo
    print("Backend ejecutándose...")
    while True:
        time.sleep(1)