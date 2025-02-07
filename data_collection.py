import multiprocessing
import json
import time
import logging
import os
import sys
from multiprocessing.managers import BaseManager

#local import
import app.modbus_tcp as modbus_tcp

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

# Definir la clase para manejar el diccionario compartido
class RealtimeDataManager(BaseManager):
    pass
    

def host_data_collection(realtime_data, device, device_signals):
    """Hilo de recolección de datos para un dispositivo específico.

    Args:
        device (dict): diccionario con los datos del equipo
        device_signals (dict): diccionario con las señales que se leen del equipo
        realtime_data (Proxy List): lista con los datos de tiempo real del sistema
    """
    device_id = device.get("device_id")
    protocol_id = device.get("protocol_id")
    if protocol_id == 0: # ModbusTcpClient
            logging.info(f"start connection to device {device_id}")
            modbus_tcp.client(realtime_data, device, device_signals)
    elif protocol_id == 1: # Mqtt
        pass
    elif protocol_id == 2: # dds
        pass
    else:
        logging.warning(f"Unknown protocol_id {protocol_id} for device {device_id}")


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



if __name__ == "__main__":
    manager = multiprocessing.Manager()
    realtime_data = manager.dict()
    logging.info("Creando objeto multiprocess.manager", type(realtime_data))
    # Registrar el diccionario para que pueda ser accedido por otros procesos (como Streamlit)
    RealtimeDataManager.register('get_realtime_data', callable=lambda: realtime_data)
    logging.info("Método 'get_realtime_data' registrado con éxito.")

    # Iniciar el servidor que expondrá los datos
    server = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')

    try:
        server.start()
        logging.info(f"Backend ejecutándose en 127.0.0.1:50000...")

        # Cargar configuraciones
        iot_devices = load_json("data/config_iot/devices.json")
        iot_protocols = load_json("data/config_iot/protocols.json")
        iot_signals = load_json("data/config_iot/signals.json")
        signals_group = load_json("data/config_iot/groups.json")

        # Iniciar la recolección de datos
        for device in iot_devices:
            if device["enabled"]:
                device_signals = next((m["device_signals"] for m in iot_signals if m["device_id"] == device["device_id"]), ["Unknown"])

                process = multiprocessing.Process(
                    target=host_data_collection,
                    args=(realtime_data, device, device_signals), 
                    daemon=True
                )
                process.start()
                logging.info(f"datacollection.main: Proceso iniciado para el dispositivo {device['device_id']}: {device['device_name']}")

        # Mantener el backend activo
        logging.info(f"datacollection.main: Backend ejecutándose...")
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        # Captura la interrupción de Ctrl+C para terminar el proceso de manera controlada
        logging.info("datacollection.main exception: Interrupción detectada (Ctrl+C), cerrando la aplicación.")
        server.shutdown()
        sys.exit(0)  # Termina el script de manera limpia
    except Exception as e:
        logging.error(f"datacollection: Unexpected error for BaseManager: {e}")
        logging.info("datacollection: Shutting down server ...")
        server.shutdown()
        sys.exit(1)  # Termina con un código de error