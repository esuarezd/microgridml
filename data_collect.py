import json

def load_json(path):
    with open(path, 'r') as file:
        data_json = json.load(file)
    return data_json
