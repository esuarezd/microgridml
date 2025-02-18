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
    
def read_analog_delta(signal_id, delta_time):
    conn, cursor = connect_db()
    # if timestamp is datetime: 
    # cursor.execute('SELECT * FROM analog WHERE signal_id = ? AND timestamp >= datetime("now", ?)', (signal_id, delta_time))
    # if timestamp is real:
    cursor.execute('SELECT * FROM analog WHERE signal_id = ? AND timestamp >= strftime("%s", "now", ?)', (signal_id, delta_time))
    data = cursor.fetchall()
    conn.close()
    return data

def read_analog(signal_id, time_initial, time_final):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM analog WHERE signal_id = ? AND timestamp >= ? AND timestamp <= ?', (signal_id, time_initial, time_final))
    data = cursor.fetchall()
    conn.close()
    return data
