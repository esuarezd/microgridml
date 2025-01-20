import time
import modbus_client
import utils

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
            signal_type = signal["signal_type"]
            signal_id = signal["signal_id"]
            obj_path = signal["obj_path"]
            signals_data[signal_id] = {
                "signal_id": signal_id, "signal_type": signal_type, "obj_path": "PV", "device_name": device_name, "value": 0, "timestamp": 0, "quality": 0, "source": 0
            }
    return signals_data

def host_data_collection(device_id, device, signals):
    """Hilo de recolección de datos para un dispositivo específico."""
    global realtime_data 
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    while True:
        try:
            match protocol_id:
                case 0:  # ModbusTcpClient
                    results = modbus_client.get_signals(device_id, device, signals)
                    print(f"Datos del dispositivo {device_id}: {results}")
                    update_realtime_data(device_id, signals, results)
                case 1:  # mqtt
                    pass
                case 2:  # dds
                    pass
                case _:
                    timestamp = utils.get_timestamp()
                    print(f"{timestamp}: Advertencia. Protocolo_id {device_id}: no encontrado")
        except ConnectionError as ce:
            timestamp = utils.get_timestamp()
            print(f"{timestamp}: Conexión perdida para el dispositivo {device_id}: {ce}")
            device["connection_status"] = "Disconnected"
        except Exception as e:
            timestamp = utils.get_timestamp()
            print(f"{timestamp}: Error inesperado para el dispositivo {device_id}: {e}")
        finally:
            time.sleep(interval)

"""
def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    modbus_client.close_all_connections()
"""
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
    return device_data
    
def update_realtime_data(device_id, signals, results):
