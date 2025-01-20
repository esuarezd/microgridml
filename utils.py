import json
from datetime import datetime

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

def get_timestamp():
    """Devuelve la hora local en un formato legible con zona horaria."""
    timestamp = datetime.now().timestamp() # Ejemplo: 1672531199.123456

    # Convertir el timestamp a un objeto datetime
    dt = datetime.fromtimestamp(timestamp)

    # Formatear con milisegundos
    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]  # .%f incluye microsegundos, [:3] deja milisegundos

    return formatted_time

def create_realtime(iot_signals):
    realtime_data = {}

    for signal in iot_signals:
        signal_id = signal["signal_id"]
        
        realtime_data[signal_id] = {
            "device": {**device, "protocol_name": protocol_name, "connection_status": "Unknown"},
            "signals": {
                "signal_id": 3, "signal_type": 1, "obj_path": "PV", "slave": 1, "function_code":"04", "address": 0, "name": "Cell Irradiance in W/m2", "data_type": "uint16", "scale_factor": 0.1, "offset": 0, "physical_range": "0 to 1500 W/m2", "data_range": "0 to 65535"
            }
        }
    return realtime_data