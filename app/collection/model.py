import sqlite3

dbfile = 'data/sqlite3/data.db'

def connect_db():
    conn = sqlite3.connect(dbfile)
    return conn, conn.cursor()

def insert_sensor(signal_id, name, signal_type, unit, physical_range, sensor_type, group_id, path1, path2):
    conn, cursor = connect_db()
    
    # Verificar si el id ya existe en la tabla sensor
    cursor.execute("SELECT COUNT(*) FROM sensor WHERE signal_id = ?", (signal_id,))
    if cursor.fetchone()[0] > 0:
        # Si el id ya existe, hacer un UPDATE
        cursor.execute('''
            UPDATE sensor
            SET name = ?, signal_type = ?, unit = ?, physical_range = ?, sensor_type = ?, group_id = ?, path1 = ?, path2 = ?
            WHERE signal_id = ?
        ''', (name, signal_type, unit, physical_range, sensor_type, group_id, path1, path2, signal_id))
    else:
        # Si el id no existe, hacer un INSERT
        cursor.execute('''
            INSERT INTO sensor (signal_id, name, signal_type, unit, physical_range, sensor_type, group_id, path1, path2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (signal_id, name, signal_type, unit, physical_range, sensor_type, group_id, path1, path2))

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
        INSERT INTO his_message (signal_id, timestamp, quality_code, user_id)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, quality_code, user_id))
    conn.commit()
    conn.close()

def insert_analog(signal_id, timestamp, value, quality_code):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO his_analog (signal_id, timestamp, value, quality_code)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, value, quality_code))
    conn.commit()
    conn.close()

def insert_discrete(signal_id, timestamp, value, quality_code):
    conn, cursor = connect_db()
    cursor.execute('''
        INSERT INTO his_discrete (signal_id, timestamp, value, quality_code)
        VALUES (?, ?, ?, ?)
    ''', (signal_id, timestamp, value, quality_code))
    conn.commit()
    conn.close()

def read_his_analog(signal_id, time_initial, time_final):
    conn, cursor = connect_db()
    cursor.execute('SELECT timestamp, value FROM his_analog WHERE signal_id = ? AND timestamp >= ? AND timestamp <= ?', (signal_id, time_initial, time_final))
    data = cursor.fetchall()
    conn.close()
    return data

def read_sensor_path1(signal_type):
    conn, cursor = connect_db()
    cursor.execute('SELECT path1 FROM sensor WHERE signal_type = ?', (signal_type,))
    data = cursor.fetchall()
    conn.close()
    return data

def read_sensor_path2(signal_type, path1):
    conn, cursor = connect_db()
    cursor.execute('SELECT path2 FROM sensor WHERE signal_type = ? AND path1 = ?', (signal_type, path1))
    data = cursor.fetchall()
    conn.close()
    return data

def read_sensor_name(signal_type, path1, path2):
    conn, cursor = connect_db()
    cursor.execute('SELECT name FROM sensor WHERE signal_type = ? AND path1 = ? AND path2 = ?', (signal_type, path1, path2))
    data = cursor.fetchall()
    conn.close()
    return data

def read_sensor_signal_id(signal_type, path1, path2, sensor_selected):
    conn, cursor = connect_db()
    cursor.execute('SELECT signal_id FROM sensor WHERE signal_type = ? AND path1 = ? AND path2 = ? AND name = ?', (signal_type, path1, path2, sensor_selected))
    data = cursor.fetchall()
    conn.close()
    return data

def read_sensor_unit(signal_type, path1, path2, sensor_selected):
    conn, cursor = connect_db()
    cursor.execute('SELECT unit FROM sensor WHERE signal_type = ? AND path1 = ? AND path2 = ? AND name = ?', (signal_type, path1, path2, sensor_selected))
    data = cursor.fetchall()
    conn.close()
    return data