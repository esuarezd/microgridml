import json
import time

def load_json(file_path):
    """Carga un archivo JSON."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_localtime():
    timestamp = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    return formatted_time