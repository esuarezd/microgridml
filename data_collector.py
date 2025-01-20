import time
import modbus_client
import utils

def preprocess_configuration(iot_devices, iot_protocols, iot_signals):
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

def host_data_collection(device_id, device, signals):
    """Hilo de recolección de datos para un dispositivo específico."""
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    while True:
        try:
            match protocol_id:
                case 0:  # ModbusTcpClient
                    results = modbus_client.get_signals(device_id, device, signals)
                    print(f"Datos del dispositivo {device_id}: {results}")
                case 1:  # mqtt
                    pass
                case 2:  # dds
                    pass
                case _:
                    timestamp = utils.get_localtime()
                    print(f"{timestamp}: Advertencia. Protocolo_id {device_id}: no encontrado")
        except ConnectionError as ce:
            timestamp = utils.get_localtime()
            print(f"{timestamp}: Conexión perdida para el dispositivo {device_id}: {ce}")
            device["connection_status"] = "Disconnected"
        except Exception as e:
            timestamp = utils.get_localtime()
            print(f"{timestamp}: Error inesperado para el dispositivo {device_id}: {e}")
        finally:
            time.sleep(interval)

def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    modbus_client.close_all_connections()
