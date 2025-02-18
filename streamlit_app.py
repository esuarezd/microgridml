from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import os

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
    st.write(realtime_data)

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
    d = st.date_input("initial date", datetime.date(2019, 7, 6))
    st.write("date selected:", d)
    data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
        'sensor': np.random.choice(['Sensor 1', 'Sensor 2', 'Sensor 3'], size=100),
        'valor': np.random.random(100) * 100
    }
    df_data = pd.DataFrame(data)
    # Selección del sensor
    sensor_selected = st.selectbox("Elige el sensor", df_data['sensor'].unique())

    # Rango de tiempo predefinido o personalizado
    time_range = st.selectbox(
        "Elige un rango de tiempo",
        ['Últimos 2 días', 'Últimos 7 días', 'Últimos 30 días', 'Último mes', 'Rango personalizado']
    )


elif st.session_state["page"] == "devices":
    st.title("Microgrid ML")
    st.write("Equipos IoT del sistema.")
    
    # Lista de llaves que deseas mostrar
    devices_list = build_devices_list()
    
    df_devices = pd.DataFrame(devices_list)
    st.dataframe(df_devices)