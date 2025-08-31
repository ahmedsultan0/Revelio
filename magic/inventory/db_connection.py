import sqlite3
import os 
from revelio import global_index
from magic.console_utils import console, general_text_format

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
    try:
        cursor.execute(f"SELECT path, name, size_mb, size_category, file_type FROM files")
        query_result = cursor.fetchall() 

        for row in query_result:

            formatted_row = {
                "path": row[0],
                "name": row[1],
                "size_mb": row[2],
                "size_category": row[3],
                "file_type": row[4]
            }

            global_index["size"][row[3]].append(row[1])
            global_index["type"].setdefault(row[3], []).append(row[1])    
            global_index["name"].append(row[1])
            global_index["path"].append(formatted_row)
            
    except Exception as e:
        console.print(general_text_format(f"Error loading files archive from DB", "error"))