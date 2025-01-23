import multiprocessing
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

def preprocess_configuration_devices(iot_devices, iot_protocols, iot_signals):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    device_data = {}

    for device in iot_devices:
        device_id = device["device_id"]
        protocol_id = device["protocol_id"]

        signals = next((m["signals"] for m in iot_signals if m["device_id"] == device_id), [])
        protocol_name = next((m["protocol_name"] for m in iot_protocols if m["protocol_id"] == protocol_id), "Unknown")

        device_data[device_id] = {
            "device": {**device, "protocol_name": protocol_name, "connection_status": "Unknown"},
            "signals": signals
        }
    logging.info(f"Device data preprocessed: {device_data}")
    return device_data

def preprocess_configuration_signals(iot_devices, iot_signals):
    """Construye una estructura preprocesada para acceso rápido a los datos."""
    signals_data = {}

    for iot_signal in iot_signals:
        device_id = iot_signal["device_id"]
        device_name = next((m["device_name"] for m in iot_devices if m["device_id"] == device_id), "Unknown")
        signals = iot_signal["signals"]
        for signal in signals:
            signal_id = signal["signal_id"]
            signal_name = signal["signal_name"]
            signal_type = signal["signal_type"]
            unit = signal["unit"]
            obj_path = signal["obj_path"]
            physical_range = signal["physical_range"]
            signals_data[signal_id] = {
                "signal_id": signal_id, "signal_name": signal_name, "signal_type": signal_type, 
                "obj_path": obj_path, "unit": unit, "device_id": device_id, "device_name": device_name, 
                "value": 0, "timestamp": 0, "quality": 0, "source": 0, "physical_range": physical_range
            }
    logging.info(f"Signals data preprocessed: {signals_data}")
    return signals_data

def host_data_collection(device_id, device, signals, shared_realtime_data):
    """Hilo de recolección de datos para un dispositivo específico.""" 
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    while True:
        try:
            match protocol_id:
                case 0:  # ModbusTcpClient
                    results = modbus_client.get_signals(device_id, device, signals)
                    logging.info(f"Device {device_id} data collected: {results}")
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


def start_data_collection(shared_realtime_data):
    """Inicia la recolección de datos."""
    # Cargar configuraciones
    iot_devices = utils.load_json("config_iot_devices.json")
    iot_protocols = utils.load_json("config_iot_protocols.json")
    iot_signals = utils.load_json("config_iot_signals.json")

    # preprocesar configuraciones
    #device_data = data_collector.preprocess_configuration_devices(iot_devices, iot_protocols, iot_signals)
    #realtime_data = data_collector.preprocess_configuration_signals(iot_devices, iot_signals)
    # Iniciar hilos de recolección de datos para dispositivos habilitados
    
    for device in iot_devices:
        if device["enabled"]:
            multiprocessing.Process(
                target=host_data_collection,
                args=(device["device_id"], device, iot_signals, shared_realtime_data),
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