import sqlite3

dbfile = 'data/sqlite3/data.db'

def conectar_db():
    conn = sqlite3.connect(dbfile)
    return conn, conn.cursor()

def crear_tabla():
    conn, cursor = conectar_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            valor REAL
        )
    ''')
    conn.commit()
    conn.close()

def insertar_dato(valor):
    conn, cursor = conectar_db()
    cursor.execute('''
        INSERT INTO datos (valor)
        VALUES (?)
    ''', (valor,))
    conn.commit()
    conn.close()

def crear_tabla_estudiantes():
    conn, cursor = conectar_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes (
            apellido TEXT,
            nombre TEXT,
            codigo TEXT PRIMARY KEY,
            nota REAL
        )
    ''')
    conn.commit()
    conn.close()