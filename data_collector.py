import time
import threading
import modbus_client

def get_protocol_name(protocol_id, iot_protocols):
    """ obj : a partir de un id retornar el nombre del protocolo   
    protocol_id: int
    iot_protocols : list of dics
    recorrido por iot_protocols para leer el nombre del protocolo """
    for protocol in iot_protocols:
        if (protocol["protocol_id"] == protocol_id):
            protocol_name = protocol["protocol_name"]
            break
    else:
        protocol_name = "Unknown protocol"
    return protocol_name

def preprocess_configuration(iot_devices, iot_signals):
    """ obj: Construye una estructura preprocesada para acceso rápido a los datos.
    parameters: 
    iot_devices: list
    iot_signals: list
    return:
    dict con la union de las dos listas """
    data_devices = {}

    for device in iot_devices:
        device_id = device["device_id"]
        signals = next((m["signals"] for m in iot_signals if m["device_id"] == device_id), [])
        data_devices[device_id] = {
            "device": device,
            "signals": signals
        }
    return data_devices

def host_data_collection(device_id, data_devices):
    """Hilo de recolección de datos para un dispositivo específico."""
    device_info = data_devices[device_id]
    device = device_info["device"]
    signals = device_info["signals"]
    interval = device["interval"]

    while True:
        try:
            match device["protocol_id"]:
                case 0: #ModbusTcpClient
                    results = modbus_client.get_signals(device_id, device, signals)
                    print(f"Datos del dispositivo {device_id}: {results}")
                case 1: #mqtt
                    pass
        except Exception as e:
            print(f"Error al leer datos del dispositivo {device_id}: {e}")
        time.sleep(interval)


