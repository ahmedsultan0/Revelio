import sqlite3
import os 
from revelio import global_index
from magic.utils.console_utils import console, general_text_format

DB_FILE = "revelio.db"

db_exists = os.path.exists(DB_FILE)

connection = sqlite3.connect("revelio.db")
cursor = connection.cursor()

if not db_exists:
    cursor.execute('''
        CREATE TABLE files (
            id TEXY(40) PRIMARY KEY,
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
        cursor.execute(f"SELECT id, path, name, size_mb, size_category, file_type FROM files")
        query_result = cursor.fetchall() 

        for row in query_result:

            formatted_row = {
                "id": row[0],
                "path": row[1],
                "name": row[2],
                "size_mb": row[3],
                "size_category": row[4],
                "file_type": row[5]
            }

            global_index["records"][row[0]] = formatted_row
            global_index["size"][row[4]].append(row[0])
            global_index["type"].setdefault(row[5], []).append(row[0])    
            global_index["name"].append(row[2])
            global_index["name_to_id"][row[2]] = row[0]
            
    except Exception as e:
        console.print(general_text_format(f"Error loading files archive from DB", "error"))