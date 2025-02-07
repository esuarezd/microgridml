import os
from datastructure.list import array_list as array_list

# Directorio de datos de los archivos
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/data/'

def new_logic():
    # Creación del catalogo vacio
    config_iot = {
        "devices": None,
        "protocols": None,
        "groups": None,
        "signals": None
    }

    # Inicialización de las estructuras de datos
    config_iot["devices"] = array_list.new_list()
    config_iot["protocols"] = array_list.new_list()
    config_iot["groups"] = array_list.new_list()
    config_iot["signals"] = array_list.new_list()

    return config_iot

def load_iot_devices(config_iot, filename):
    devices = config_iot["devices"]
    devices_file = os.path.join(data_dir, filename)
    config_iot["devices"] = array_list.load_list(devices, devices_file)
    return device_size(config_iot)

def device_size(config_iot):
    return array_list.size(config_iot["devices"])

def load_iot_protocols(config_iot, filename):
    protocols = config_iot["protocols"]
    protocols_file = os.path.join(data_dir, filename)
    config_iot["protocols"] = array_list.load_list(protocols, protocols_file)
    return protocols_size(config_iot)

def protocols_size(config_iot):
    return array_list.size(config_iot["protocols"])

def load_iot_groups(config_iot, filename):
    groups = config_iot["groups"]
    groups_file = os.path.join(data_dir, filename)
    config_iot["groups"] = array_list.load_list(groups, groups_file)
    return groups_size(config_iot)

def groups_size(config_iot):
    return array_list.size(config_iot["groups"])

def load_iot_signals(config_iot, filename):
    signals = config_iot["signals"]
    signals_file = os.path.join(data_dir, filename)
    config_iot["signals"] = array_list.load_list(signals, signals_file)
    return groups_size(config_iot)

def signals_size(config_iot):
    return array_list.size(config_iot["signals"])