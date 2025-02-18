# script to create tables in sqlite3 database
import sqlite3

dbfile = 'data/sqlite3/data.db'

create_table_sensor = '''
CREATE TABLE sensor (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    data_type TEXT NOT NULL,
    unit TEXT,
    physical_range TEXT,
    sensor_type TEXT,
    group_id INTEGER,
    path1  TEXT,
    path2  TEXT
);
'''

create_table_user = '''
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
'''

create_table_message = '''
CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id INTEGER NOT NULL,
    timestamp REAL NOT NULL,
    quality_code INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (signal_id) REFERENCES sensor(id) 
);
'''

create_table_analog = '''
CREATE TABLE analog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id INTEGER NOT NULL,
    timestamp REAL NOT NULL,                    
    value REAL NOT NULL,                        
    quality_code INTEGER NOT NULL,              
    FOREIGN KEY (signal_id) REFERENCES sensor(id)  
);
'''

create_table_discrete = '''
CREATE TABLE discrete (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_id INTEGER NOT NULL,
    timestamp REAL NOT NULL,
    value INTEGER NOT NULL,
    quality_code INTEGER NOT NULL,
    FOREIGN KEY (signal_id) REFERENCES sensor(id) 
);
'''

scripts_create = [create_table_sensor, create_table_user, create_table_message, create_table_analog, create_table_discrete]
table_names = ['sensor', 'user', 'message', 'analog', 'discrete']

def connnect_db():
    conn = sqlite3.connect(dbfile)
    return conn, conn.cursor()

def create_tables():
    conn, cursor = connnect_db()
    for script in scripts_create:
        cursor.execute(script)
    conn.commit()
    conn.close()
   
def drop_tables():
    conn, cursor = connnect_db()
    for script in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {script}")
        print(f'drop table: {script}')
    conn.commit()
    conn.close()
 
def main():
    drop_tables()
    create_tables()
    print('Tables created successfully')

if __name__ == '__main__':
    main()