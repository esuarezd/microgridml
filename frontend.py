import multiprocessing
import time
from multiprocessing.managers import BaseManager
import logging

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler("logs/frontend.log", mode="a")  # Registrar en un archivo
    ]
)

# Definir la clase para manejar el diccionario compartido en el front-end
class RealtimeDataManager(BaseManager):
    pass

def query_realtime_data():
    try:
        logging.info("Conectando con el servidor BaseManager...")
        # Conectar al servidor BaseManager en el mismo puerto
        manager = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
        manager.connect()
        logging.info("Conexión exitosa con el servidor.")

        # Obtener el diccionario de datos en tiempo real
        realtime_data = manager.get_realtime_data()
        logging.info(f"tipo de dato {type(realtime_data)}")

        while True:
            # Consultar el dato que está leyendo
            # Puedes acceder a los datos usando 'realtime_data' (diccionario compartido)
            for group_id, data in realtime_data.items():
                logging.info(f"Datos del grupo {group_id}: {data}")

            # Esperar un segundo antes de hacer otra consulta
            time.sleep(1)

    except Exception as e:
        logging.error(f"Error al conectar con el backend: {e}")

if __name__ == "__main__":
    #query_realtime_data()
    try:
        logging.info("Conectando con el servidor BaseManager...")
        # Conectar al servidor BaseManager en el mismo puerto
        manager = RealtimeDataManager(address=('127.0.0.1', 50000), authkey=b'secret')
        manager.connect()
        logging.info("Conexión exitosa con el servidor.")

        # Obtener el diccionario de datos en tiempo real
        realtime_data = manager.get_realtime_data()

        if realtime_data:
            logging.info(f"tipo de dato: {type(realtime_data)}")
        else:
            logging.warning("No se han recibido datos de tiempo real.")

        while True:
            # Consultar el dato que está leyendo
            # Puedes acceder a los datos usando 'realtime_data' (diccionario compartido)
        #    for group_id, data in realtime_data.items():
        #        logging.info(f"Datos del grupo {group_id}: {data}")

            # Esperar un segundo antes de hacer otra consulta
            time.sleep(60)

    except Exception as e:
        logging.error(f"Error al conectar con el backend: {e}")
