import subprocess
import time
import sys

def run_streamlit_app():
    # Ejecutar Streamlit en segundo plano y obtener el objeto del proceso
    process = subprocess.Popen(["streamlit", "run", "app/visualization/streamlit_app.py"])
    
    # Retornar el proceso para que puedas controlarlo más tarde (como detenerlo)
    return process

def stop_streamlit_app(process):
    # Detener el proceso de Streamlit
    process.terminate()  # Esto envía una señal para terminar el proceso (similar a Ctrl+C)
    # Si quieres forzar el cierre (en caso de que no se detenga con terminate), usa kill:
    # process.kill()

def main():
    # Ejecuta Streamlit en segundo plano
    try:
        # solucion usando subprocess.popopen()
        streamlit_process = run_streamlit_app()
        print("Streamlit está ejecutándose... Para detenerlo, presiona Ctrl+C.")
        while True:
            time.sleep(10) 
    except KeyboardInterrupt:
        # Captura la interrupción de Ctrl+C para terminar el proceso de manera controlada
        print("Interrupción detectada (Ctrl+C), cerrando la aplicación.")
        stop_streamlit_app(streamlit_process)
        sys.exit(0)  # Termina el script de manera limpia
    except Exception as e:
        print(f"Unexpected error for BaseManager: {e}")
        print("Shutting down streamlit ...")
        stop_streamlit_app(streamlit_process)
        sys.exit(1)  # Termina con un código de error
