import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'complaints.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
    print('Database initialized and tables created.')

if __name__ == '__main__':
    init_db()
