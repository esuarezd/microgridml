import json
import time

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

def get_localtime():
    """Devuelve la hora local en un formato legible con zona horaria."""
    timestamp = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", timestamp)
    return formatted_time
