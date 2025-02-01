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
            "value": 0,
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

def update_realtime_data(results, signal_index):
    """actualizar datos leidos

    Args:
        results (list): lista de datos leidos de un equipo
        signal_index (dict): _description_
    """
    for result in results:
        signal_id = result.get('signal_id')
        if signal_id in signal_index:
            signal_index[signal_id].update({
                'value': result.get('value', 0),
                'value_protocol': result.get('value_protocol', 0),
                'timestamp': result.get('timestamp', 0),
                'quality': result.get('quality', 0),
                'source': result.get('source', 0)
            })
        else:
            logging.warning(f"Signal ID {signal_id} not found in indexed data.")
 
    

def host_data_collection(device, device_signals, shared_realtime_data):
    """Hilo de recolección de datos para un dispositivo específico.

    Args:
        device (dict): diccionario con los datos del equipo
        device_signals (dict): diccionario con las señales que se leen del equipo
        shared_realtime_data (dic): dicctionario con los datos de tiempo real del sistema
    """
    device_id = device["device_id"]
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    # Crear el índice de señales una sola vez
    signal_index = {signal['signal_id']: signal for signal in device_signals}


    while True:
        try:
            if protocol_id == 0:  # ModbusTcpClient
                results = modbus_client.get_signals(device, device_signals)
                logging.info(f"Device {device_id} (protocol {protocol_id}) data collected: {results}")
                # Crear un índice directo para signal_id
                
                update_realtime_data(results, signal_index)
            elif protocol_id == 1:  # MQTT
                pass  # Implementación futura para MQTT
            elif protocol_id == 2:  # DDS
                pass  # Implementación futura para DDS
            else:
                logging.warning(f"Unknown protocol_id {protocol_id} for device {device_id}")

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
    signals_group = load_json("data/config_signals_group.json")

    # preprocesar configuraciones
    for group in signals_group:
        group_id = group["group_id"]
        group_name = group["group_name"]
        if group_id == 0:
            shared_realtime_data[group_id] = preprocess_configuration_devices(iot_devices, iot_protocols, group_name)
        else:
            shared_realtime_data[group_id] = preprocess_configuration_signals(iot_signals, group_id, group_name)
    # Iniciar hilos de recolección de datos para dispositivos habilitados
    
    for device in iot_devices:
        if device["enabled"]:
            device_signals = next((m["device_signals"] for m in iot_signals if m["device_id"] == device["device_id"]), "Unknown")

            multiprocessing.Process(
                target=host_data_collection,
                args=(device, device_signals, shared_realtime_data),
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