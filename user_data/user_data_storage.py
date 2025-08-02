import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'user_data.db')


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()


def get_last_user_entry(user_id):
    return None
