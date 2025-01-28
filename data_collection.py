import multiprocessing
import json
import time
import modbus_client
import logging

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler("data_collector.log", mode="a")  # Registrar en un archivo
    ]
)


    
def preprocess_configuration_devices(iot_devices, iot_protocols, obj_path_name):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    device_data = list()

    for device in iot_devices:
        protocol_id = device["protocol_id"]

        protocol_name = next((m["protocol_name"] for m in iot_protocols if m["protocol_id"] == protocol_id), "Unknown")

        device_data.append( 
            { 
            **device, 
            "protocol_name": protocol_name, 
            "obj_path_name": obj_path_name,
            "path1": device["device_name"],
            "value": "Unknown",
            "quality": 0,
            "source": 0,
            "timestamp": 0
            }
        )
    logging.info(f"Device data preprocessed: {device_data}")
    return device_data

def preprocess_configuration_signals(iot_signals, obj_path_id, obj_path_name):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    signals_data = list()

    for iot_signal in iot_signals:
        signals = iot_signal["signals"]
        for signal in signals:
            if signal["obj_path_id"] == obj_path_id:

                signals_data.append( 
                    { 
                    **signal, 
                    "obj_path_name": obj_path_name,
                    "value": "Unknown",
                    "quality": 0,
                    "source": 0,
                    "timestamp": 0
                    }
                )
    logging.info(f"Signals data preprocessed: {signals_data}")
    return signals_data

def update_realtime_data(results, shared_realtime_data):
    for signal_id, result_info in results.items():
        if signal_id in shared_realtime_data:
            sensor = shared_realtime_data[signal_id]
            sensor['value'] = result_info['value'] 
            sensor['timestamp'] = result_info['timestamp']
            sensor['quality'] = result_info['quality']
            sensor['source'] = result_info['source']
        else:
            logging.warning(f"Signal ID {signal_id} not found in realtime_data.")

def host_data_collection(device, iot_signals, shared_realtime_data):
    """Hilo de recolección de datos para un dispositivo específico.""" 
    device_id = device["device_id"]
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    while True:
        try:
            match protocol_id:
                case 0:  # ModbusTcpClient
                    results = modbus_client.get_signals(device, iot_signals)
                    logging.info(f"Device {device_id} protocol {protocol_id} data collected: {results}")
                    update_realtime_data(results, shared_realtime_data)
                case 1:  # mqtt
                    pass
                case 2:  # dds
                    pass
                case _:
                    logging.warning(f"Unknown protocol_id {device_id}")
        except ConnectionError as ce:
            logging.error(f"Connection lost for device {device_id}: {ce}")
            device["connection_status"] = "Disconnected"
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
    obj_paths = load_json("data/config_obj_paths.json")

    # preprocesar configuraciones
    for obj_path in obj_paths:
        obj_path_id = obj_path["obj_path_id"]
        obj_path_name = obj_path["obj_path_name"]
        if obj_path_id == 0:
            shared_realtime_data[obj_path_id] = preprocess_configuration_devices(iot_devices, iot_protocols, obj_path_name)
        else:
            shared_realtime_data[obj_path_id] = preprocess_configuration_signals(iot_signals, obj_path_id, obj_path_name)
    # Iniciar hilos de recolección de datos para dispositivos habilitados
    
    for device in iot_devices:
        if device["enabled"]:
            multiprocessing.Process(
                target=host_data_collection,
                args=(device, iot_signals, shared_realtime_data),
                daemon=True
            ).start()
            logging.info(f"Proceso iniciado para el dispositivo {device['device_id']}: {device['device_name']}")

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    realtime_data = manager.dict()

    # Iniciar la recolección de datos
    start_data_collection(realtime_data)

    # Mantener el backend activo
    print("Backend ejecutándose...")
    while True:
        time.sleep(1)