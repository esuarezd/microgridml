import os

import app.collection.logic as logic

# Definir la ruta del directorio de logs 
log_dir = 'logs/collection'

# Crear las carpetas 'logs' y 'logs/collection' si no existen
os.makedirs(log_dir, exist_ok=True)

# Definir la ruta del directorio de la base de datos 
db_dir = 'data/sqlite3'

# Crear las carpetas 'logs' y 'logs/collection' si no existen
os.makedirs(db_dir, exist_ok=True)
    
# Main function
def main():
    logic.main()


# Main function call to run the program
if __name__ == '__main__':
    main()