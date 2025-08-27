import sqlite3
import os 
from revelio import global_index

DB_FILE = "revelio.db"

db_exists = os.path.exists(DB_FILE)

connection = sqlite3.connect("revelio.db")
cursor = connection.cursor()

if not db_exists:
    cursor.execute('''
        CREATE TABLE files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL UNIQUE,
            size_mb NUMBERIC,
            size_category TEXT,
            file_type TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()


def sync_dictionary_with_db(data_list, keys, table_name):
    """
    Syncs a list with a database table.
    
    Parameters:
    - data_list: containing dictionary items to sync.
    - keys: A list of key names in the dictionary to map to the database columns.
    - table_name: Name of the database table to sync with.
    """

    for item in data_list:
        try:
            columns = ', '.join(keys)
            values = list(item.values())
            placeholders = ', '.join(['?' for _ in keys])
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(insert_query, values)
        except sqlite3.IntegrityError:
            continue

    connection.commit()

def load_all_from_table():
    """
    Loads categorized records from a the files database table.
    """
    cursor.execute(f"SELECT name, path, size_category, file_type, size_mb FROM files")
    query_result = cursor.fetchall() 

    for row in query_result:

        formatted_row = {
            "name": row[0],
            "path": row[1],
            "size_category": row[2],
            "file_type": row[3],
            "size_mb": row[4]
        }

        global_index["size"][row[2]].append(formatted_row)
        global_index["type"].setdefault(row[3], []).append(formatted_row)    
        global_index["name"].append(row[0])
        global_index["path"].append(row[1])
    