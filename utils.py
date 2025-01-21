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