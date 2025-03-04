from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import streamlit as st
import time

import app.visualization.logic as logic

# Definir la ruta del directorio de logs 
log_dir = 'logs/visualization'

# Crear las carpetas 'logs' y 'logs/visualization' si no existen
os.makedirs(log_dir, exist_ok=True)

def new_iot_system():
    app = logic.new_iot_system()
    return app

def load_data(app):
    logic.load_data(app)

def connect_to_realtime_data():
    realtime_data = logic.connect_to_realtime_data()
    return realtime_data

def build_devices_list():
    output = logic.build_devices_list(app)
    return output

def build_group_list(group_id):
    output = logic.build_group_list(group_id, app, realtime_data)
    return output

# Configuración de la página
st.set_page_config(
    layout="wide",
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

try:
    app = new_iot_system()
    load_data(app)
    realtime_data = connect_to_realtime_data()

except Exception as e:
    st.error(f"Error conectando a datos en tiempo real: {e}")
    

# Inicializar el estado de navegación
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Sidebar con botones para navegar
if st.sidebar.button("home"):
    st.session_state["page"] = "home"
if st.sidebar.button("measures"):
    st.session_state["page"] = "measures"
if st.sidebar.button("history"):
    st.session_state["page"] = "history"
if st.sidebar.button("devices"):
    st.session_state["page"] = "devices"
    
# Navegación entre páginas
if st.session_state["page"] == "home":
    st.title("Microgrid ML")
    #st.write(realtime_data)

    # Configuración del Dashboard

    # Sección de estado general
    col1, col2, col3 = st.columns(3)
    col1.metric("status", "OK")
    col2.metric("Local time", time.strftime("%H:%M"))
    col3.metric("Last update", "Realtime")

    # Sección de medición de energía
    st.subheader("Energy Status")

    col1, col2, col3 = st.columns(3)

    # Carga de batería
    stateofcharge = realtime_data[24]["value"]  # Simula porcentaje de batería
    col1.metric("🔋 Battery charge", f"{stateofcharge} %")
    # col1.progress(stateofcharge / 100)
    batterypower = realtime_data[20]["value"]
    col1.metric("🔋 Battery power",f"{batterypower} W")
    

    # Potencia del cargador solar
    pv_power = realtime_data[17]["value"]
    col2.metric("☀️ PV Charger", f"{pv_power} W")

    # Potencias en inversor
    inputpower1 = realtime_data[37]["value"]
    inputpower2 = realtime_data[38]["value"]
    inputpower3 = realtime_data[39]["value"]
    inputpower = inputpower1 + inputpower2 + inputpower3
    outputpower1 = realtime_data[49]["value"]
    outputpower2 = realtime_data[50]["value"]
    outputpower3 = realtime_data[51]["value"]
    outputpower = outputpower1 + outputpower2 + outputpower3
    outputfrequency = realtime_data[48]["value"]
    col3.metric("⚡ AC input", f"{inputpower} W")
    col3.metric("🔌 AC output", f"{outputpower} W")

    # Simulación de actualización
    st.session_state["page"] = "home"

if st.session_state["page"] == "measures":
    st.title("Microgrid ML")
    st.write("Generation measures")
    # Lista de llaves que deseas mostrar
    group_1_list = build_group_list(1)
    df_group_1 = pd.DataFrame(group_1_list)
    st.dataframe(df_group_1) 
    
    st.write("Energy Storage measures")
    # Lista de llaves que deseas mostrar
    group_2_list = build_group_list(2)
    df_group_2 = pd.DataFrame(group_2_list)
    st.dataframe(df_group_2) 
    
    st.write("PCC measures")
    # Lista de llaves que deseas mostrar
    group_3_list = build_group_list(3)
    df_group_3 = pd.DataFrame(group_3_list)
    st.dataframe(df_group_3) 
    
    st.write("DBI measures")
    # Lista de llaves que deseas mostrar
    group_4_list = build_group_list(4)
    df_group_4 = pd.DataFrame(group_4_list)
    st.dataframe(df_group_4) 

elif st.session_state["page"] == "history":
    st.title("Microgrid ML")
    st.write("measurement history")
    
    data_path1 = logic.read_analog_path1()
    df_data1 = pd.DataFrame(data_path1)
    path1 = st.selectbox("path 1", df_data1[0].unique())
    
    data_path2 = logic.read_analog_path2(path1)
    df_data2 = pd.DataFrame(data_path2)
    path2 = st.selectbox("path 2", df_data2[0].unique())
    
    data_sensors = logic.read_analog_names(path1, path2)
    df_sensors = pd.DataFrame(data_sensors)
    sensor_selected = st.selectbox("Sensor", df_sensors[0].unique())
    
    data_signal_id = logic.read_analog_signal_id(path1, path2, sensor_selected)
    signal_id = data_signal_id[0][0]
    
    data_unit = logic.read_analog_unit(path1, path2, sensor_selected)
    unit = data_unit[0][0]

    # Rango de tiempo predefinido o personalizado
    time_range = st.selectbox(
        "Time range",
        ['Last hour', 'Last day', 'Last 2 days', 'Last 7 days', 'Last 30 days', 'Yesterday', 'Custom']
    )
    
    # Filtrar datos por el rango de tiempo y el sensor seleccionado
    if time_range == 'Last hour':
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(hours=1)
    elif time_range == 'Last day':
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(days=1)
    elif time_range == 'Last 2 days':
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(days=2)
    elif time_range == 'Last 7 days':
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(days=7)
    elif time_range == 'Last 30 days':
        end_datetime = datetime.now()
        start_datetime = end_datetime - timedelta(days=30)
    elif time_range == 'Yesterday':
        end_datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # inicio de hoy
        start_datetime = end_datetime - timedelta(days=1)  # inicio de ayer a las 00:00:00
        end_datetime = end_datetime - timedelta(seconds=1)
    elif time_range == 'Custom':
        start_date = st.date_input('Initial date', datetime.today())
        start_time = st.time_input('Initial time', datetime.now()) 
        
        end_date = st.date_input('Final date', datetime.today())
        end_time = st.time_input('Final time', datetime.now())
        
        #imprimir 
        #st.write("Start date: ", start_date, "Time: ", start_time)
        #st.write("End date: ", end_date, "Time: ", end_time)
        #st.write("Start date : ", start_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Combina la fecha y la hora
        start_datetime = datetime.combine(start_date, start_time)  # Combina fecha y hora de inicio
        end_datetime = datetime.combine(end_date, end_time)  # Combina fecha y hora de fin

    
    # Convertir a epoch time
    start_timestamp = start_datetime.timestamp()
    end_timestamp = end_datetime.timestamp()
    
    # Mostrar las fechas y horas seleccionadas
    st.write("Initial timestamp :", start_datetime, start_timestamp)
    st.write("Final timestamp :", end_datetime, end_timestamp)
    
    #hacemos la consulta
    data_his_analog = logic.read_his_analog(signal_id, start_timestamp, end_timestamp)
    df_data_his_analog = pd.DataFrame(data_his_analog, columns=['timestamp', 'value'])
    
    # Convertir el timestamp a fechas legibles (en este caso, segundos)
    #df_data_his_analog['datetime'] = pd.to_datetime(df_data_his_analog['timestamp'], unit='s', utc=True)
    
    # Convertir a la zona horaria local (si está en UTC y necesitas convertirlo a tu zona local)
    #df_data_his_analog['datetime'] = df_data_his_analog['datetime'].dt.tz_convert('America/Bogota')
    
    df_data_his_analog['datetime'] = df_data_his_analog['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    
    # agregamos la columna unidades
    df_data_his_analog['unit'] = unit
    
    #mostramos el panda en la pagina web
    st.write(df_data_his_analog[['datetime', 'value', 'unit']])
    
    # Graficar los datos
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_data_his_analog['datetime'], df_data_his_analog['value'], label=sensor_selected, color='b')
    ax.set_title(f"sensor {sensor_selected} [{unit}]")
    ax.set_xlabel('datetime')
    ax.set_ylabel(f'value in {unit}')
    ax.grid(True)
    ax.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


elif st.session_state["page"] == "devices":
    st.title("Microgrid ML")
    st.write("Equipos IoT del sistema.")
    
    # Lista de llaves que deseas mostrar
    devices_list = build_devices_list()
    
    df_devices = pd.DataFrame(devices_list)
    st.dataframe(df_devices)