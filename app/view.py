"""
 * Copyright 2024, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollo para la microrred del edificio Mario Laserna
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 * contribuciones:
 *
 * Edison Suarez - Version inicial
 """


import app.logic as logic

def new_logic():
    app = logic.new_logic()
    return app

def load_iot_devices(app):
    iot_devices = logic.load_iot_devices(app, "config_iot/devices.json")
    return iot_devices

def load_iot_protocols(app):
    iot_protocols = logic.load_iot_protocols(app, "config_iot/protocols.json")
    return iot_protocols

def load_iot_groups(app):
    iot_groups = logic.load_iot_groups(app, "config_iot/groups.json")
    return iot_groups

def load_iot_signals(app):
    # carga de señales por equipo
    iot_signals = logic.load_iot_signals(app, "config_iot/signals.json")
    return iot_signals
    

# Se carga la configuracion iot para la aplicacion
app = new_logic()

def main():
    iot_devices = load_iot_devices(app)
    iot_protocols = load_iot_protocols(app)
    