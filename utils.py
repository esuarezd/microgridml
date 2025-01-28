
from datetime import datetime



def get_timestamp():
    """Devuelve la hora local en un formato legible con zona horaria."""
    timestamp = datetime.now().timestamp() # Ejemplo: 1672531199.123456

    # Convertir el timestamp a un objeto datetime
    dt = datetime.fromtimestamp(timestamp)

    # Formatear con milisegundos
    formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]  # .%f incluye microsegundos, [:3] deja milisegundos

    return formatted_time