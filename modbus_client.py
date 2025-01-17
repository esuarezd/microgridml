from pymodbus.client import ModbusTcpClient
from time import sleep

def connect_device(device, mapping):
    # iot_device:
    # mapping:
    client = ModbusTcpClient(device["ip_address"])
    if client.connect():
        device["connection_status"] = "OK"
        for data in mapping:
            response = client.read_input_registers(address = data["address"], slave = data["unit_id"])
            if response.isError():
                # Manejo de errores
                data["value"] = input_register[0] = f"Error leyendo registros: {response}"
            else:
                # Accede a los valores leídos
                input_register = response.registers
                sleep(2)
                data["value"] = input_register[0]
    else:
        device["connection_status"] = "Failure"
    return mapping