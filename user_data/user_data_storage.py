import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'user_data.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            weight INTEGER, hips INTEGER, thigh INTEGER,
            waist INTEGER, chest INTEGER, biceps INTEGER,
            updated_at TEXT
        )
        '''
    )
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS user_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight INTEGER, hips INTEGER, thigh INTEGER,
            waist INTEGER, chest INTEGER, biceps INTEGER,
            logged_at TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def get_last_user_entry(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''
        SELECT weight, hips, thigh, waist, chest, biceps, updated_at
        FROM users WHERE user_id = ?
        ''',
        (user_id,)
    )
    r = c.fetchone()
    conn.close()
    if not r:
        return None
    return dict(zip(
        ['weight', 'hips', 'thigh', 'waist', 'chest', 'biceps', 'timestamp'], r
    ))


def create_or_update_user(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat(timespec='seconds')
    c.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    if not c.fetchone():
        c.execute(
            '''
            INSERT INTO users (user_id, weight, hips, thigh, waist, chest, biceps, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                user_id,
                kwargs.get('weight'),
                kwargs.get('hips'),
                kwargs.get('thigh'),
                kwargs.get('waist'),
                kwargs.get('chest'),
                kwargs.get('biceps'),
                now
            )
        )
    else:
        fields, vals = [], []
        for k in ['weight', 'hips', 'thigh', 'waist', 'chest', 'biceps']:
            if k in kwargs and kwargs[k] is not None:
                fields.append(f'{k} = ?')
                vals.append(kwargs[k])
        if fields:
            vals += [now, user_id]
            c.execute(
                f'''
                UPDATE users SET {', '.join(fields)}, updated_at = ?
                WHERE user_id = ?
                ''',
                vals
            )
    conn.commit()
    conn.close()


def update_last_user_entry(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat(timespec='seconds')
    fields, vals = [], []
    for k in ['weight', 'hips', 'thigh', 'waist', 'chest', 'biceps']:
        if k in kwargs and kwargs[k] is not None:
            fields.append(f'{k} = ?')
            vals.append(kwargs[k])
    if fields:
        vals += [now, user_id]
        c.execute(
            f'''
            UPDATE users SET {', '.join(fields)}, updated_at = ?
            WHERE user_id = ?
            ''',
            vals
        )
    c.execute(
        '''
        INSERT INTO user_log (user_id, weight, hips, thigh, waist, chest, biceps, logged_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            user_id,
            kwargs.get('weight'),
            kwargs.get('hips'),
            kwargs.get('thigh'),
            kwargs.get('waist'),
            kwargs.get('chest'),
            kwargs.get('biceps'),
            now
        )
    )
    conn.commit()
    conn.close()
