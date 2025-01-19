import json

def load_json(file_path):
    """Carga un archivo JSON."""
    with open(file_path, 'r') as file:
        return json.load(file)
