import sqlite3

dbfile = 'data/sqlite3/data.db'

def connect_db():
    conn = sqlite3.connect(dbfile)
    return conn, conn.cursor()

def insert_sensor(id, name, data_type, unit, physical_range, sensor_type, group_id, path1, path2):
    conn, cursor = connect_db()
    
    # Verificar si el id ya existe en la tabla sensor
    cursor.execute("SELECT COUNT(*) FROM sensor WHERE id = ?", (id,))
    if cursor.fetchone()[0] > 0:
        # Si el id ya existe, hacer un UPDATE
        cursor.execute('''
            UPDATE sensor
            SET name = ?, data_type = ?, unit = ?, physical_range = ?, sensor_type = ?, group_id = ?, path1 = ?, path2 = ?
            WHERE id = ?
        ''', (name, data_type, unit, physical_range, sensor_type, group_id, path1, path2, id))
    else:
        # Si el id no existe, hacer un INSERT
        cursor.execute('''
            INSERT INTO sensor (id, name, data_type, unit, physical_range, sensor_type, group_id, path1, path2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, name, data_type, unit, physical_range, sensor_type, group_id, path1, path2))

    conn.commit()
    conn.close()

def insert_user(name):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO user (name)
        VALUES (?)
    ''', (name,))
    conn.commit()
    conn.close()
    
def insert_message(signal_id, timestamp, quality_code, user_id):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO message (signal_id, timestamp, quality_code, user_id)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, quality_code, user_id))
    conn.commit()
    conn.close()

def insert_analog(signal_id, timestamp, value, quality_code):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO analog (signal_id, timestamp, value, quality_code)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, value, quality_code))
    conn.commit()
    conn.close()

def insert_discrete(signal_id, timestamp, value, quality_code):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO discrete (signal_id, timestamp, value, quality_code)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, value, quality_code))
    conn.commit()
    conn.close()
    
def agregar_varios_estudiantes(estudiantes):
    conn, cursor = connect_db()
    cursor.executemany('''
        INSERT INTO estudiantes (apellido, nombre, codigo, nota)
        VALUES (?, ?, ?, ?)
    ''', estudiantes)
    conn.commit()
    conn.close()
    
def leer():
    conn, cursor = connect_db()
    intruccion = 'SELECT * FROM estudiantes'
    cursor.execute(intruccion)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    for d in data:
        print(d)
    
def read_analog():
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM analog')
    data = cursor.fetchall()
    conn.close()
    for d in data:
        print(d)
    return data

estudiantes = [
    ('Perez', 'Pedro', '1234', 4.5),
    ('Gomez', 'Maria', '1235', 3.5),
    ('Gonzalez', 'Jose', '1236', 3.0),
    ('Rodriguez', 'Ana', '1237', 4.0),
    ('Jimenez', 'Juan', '1238', 3.5),
]
#agregar_varios_estudiantes(estudiantes)

# data = read_analog()