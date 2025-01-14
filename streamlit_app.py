import streamlit as st
from config_loader import load_config
from modbus import data_collect

# Configuración de la página para usar todo el ancho disponible
st.set_page_config(
    layout="wide",  
    page_title="microgrid ml",
    page_icon="☀️"  # Ícono de sol
)

st.title("Aplicación Streamlit en Raspberry Pi")
st.write("Hola, esta es mi primera aplicación web con Streamlit en la Raspberry Pi.")

iot_devices = load_config("config_iot_devices.json")

data = data_collect(iot_devices)