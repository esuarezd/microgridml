import logging
import os
import subprocess
import time
import sys

# Verificar si la carpeta 'logs' existe, si no, crearla
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/data_visualization.log", mode="a")
    ]
)

def run_streamlit_app():
    # Ejecutar Streamlit en segundo plano y obtener el objeto del proceso
    process = subprocess.Popen(["streamlit", "run", "app/streamlit_app.py"])
    
    # Retornar el proceso para que puedas controlarlo más tarde (como detenerlo)
    return process

def stop_streamlit_app(process):
    # Detener el proceso de Streamlit
    process.terminate()  # Esto envía una señal para terminar el proceso (similar a Ctrl+C)
    # Si quieres forzar el cierre (en caso de que no se detenga con terminate), usa kill:
    # process.kill()

if __name__ == "__main__":
    # Ejecuta Streamlit en segundo plano
    try:
        # solucion usando subprocess.popopen()
        streamlit_process = run_streamlit_app()
        logging.info("data_vis.main: Streamlit está ejecutándose... Para detenerlo, presiona Ctrl+C.")
        while True:
            time.sleep(10) 
        # solucion con subprocess.run()
        # subprocess.run(["streamlit", "run", "app/streamlit_app.py"])
    except KeyboardInterrupt:
        # Captura la interrupción de Ctrl+C para terminar el proceso de manera controlada
        logging.info("data_vis.main exception: Interrupción detectada (Ctrl+C), cerrando la aplicación.")
        stop_streamlit_app(streamlit_process)
        sys.exit(0)  # Termina el script de manera limpia
    except Exception as e:
        logging.error(f"data_vis.main exception: Unexpected error for BaseManager: {e}")
        logging.info("data_vis.main exception: Shutting down streamlit ...")
        stop_streamlit_app(streamlit_process)
        sys.exit(1)  # Termina con un código de error
