from time import time, sleep
# app local
import modbus_client

def preprocess_configuration(iot_protocols, iot_devices, iot_signals):
    """ obj: Construye una estructura preprocesada para acceso rápido a los datos.
    parameters: 
    iot_protocols : list
    iot_devices: list
    iot_signals: list
    return:
    device_data: dict con la union de las listas """
    device_data = {}

    for device in iot_devices:
        device_id = device["device_id"]
        protocol_id = device["protocol_id"]

        signals = next((m["signals"] for m in iot_signals if m["device_id"] == device_id), [])
        protocol_name = next((m["protocol_name"] for m in iot_protocols if m["protocol_id"] == protocol_id), "Unknow")

        device_data[device_id] = {
            "device": device,
            "signals": signals
        }
        device_data[device_id]["device"]["protocol_name"] = protocol_name
        device_data[device_id]["device"]["connection_status"] = "Unknow"
    return device_data

def host_data_collection(device_id, device, signals):
    """Hilo de recolección de datos para un dispositivo específico."""
    
    protocol_id = device["protocol_id"]
    interval = device["interval"]

    while True:
        try:
            match protocol_id:
                case 0: #ModbusTcpClient
                    results = modbus_client.get_signals(device_id, device, signals)
                    print(f"Datos del dispositivo {device_id}: {results}")
                case 1: #mqtt
                    pass
                case 2: #dds
                    pass
                case _:
                    timestamp = time()
                    print(f"{timestamp}: Advertencia. Protocolo_id {device_id}: no encontrado")
        except Exception as e:
            timestamp = time()
            print(f"{timestamp}: Error general al leer datos del dispositivo {device_id}: {e}")
        sleep(interval)


def close_all_connections():
    """Cierra todas las conexiones abiertas."""
    modbus_client.close_all_connections()