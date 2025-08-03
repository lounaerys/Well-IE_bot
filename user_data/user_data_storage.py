import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'user_data.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            weight INTEGER, hips INTEGER, thigh INTEGER,
            waist INTEGER, chest INTEGER, biceps INTEGER,
            updated_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight INTEGER, hips INTEGER, thigh INTEGER,
            waist INTEGER, chest INTEGER, biceps INTEGER,
            logged_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_or_update_user(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    now = datetime.now().isoformat(timespec='seconds')
    c.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    if not c.fetchone():
        c.execute('''
            INSERT INTO users (user_id, weight, hips, thigh, waist, chest, biceps, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            kwargs.get('weight'),
            kwargs.get('hips'),
            kwargs.get('thigh'),
            kwargs.get('waist'),
            kwargs.get('chest'),
            kwargs.get('biceps'),
            now
        ))
    else:
        fields, vals = [], []
        for k in ['weight','hips','thigh','waist','chest','biceps']:
            if k in kwargs and kwargs[k] is not None:
                fields.append(f"{k} = ?"); vals.append(kwargs[k])
        if fields:
            vals += [now, user_id]
            c.execute(f'''
                UPDATE users SET {', '.join(fields)}, updated_at = ?
                WHERE user_id = ?
            ''', vals)
    conn.commit(); conn.close()

def get_last_user_entry(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT weight, hips, thigh, waist, chest, biceps, updated_at
        FROM users WHERE user_id = ?
    ''', (user_id,))
    r = c.fetchone()
    conn.close()
    if not r:
        return None
    return dict(zip(
        ['weight','hips','thigh','waist','chest','biceps','timestamp'], r
    ))

def update_last_user_entry(user_id, **kwargs):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    now = datetime.now().isoformat(timespec='seconds')
    fields, vals = [], []
    for k in ['weight','hips','thigh','waist','chest','biceps']:
        if k in kwargs and kwargs[k] is not None:
            fields.append(f"{k} = ?"); vals.append(kwargs[k])
    if fields:
        vals += [now, user_id]
        c.execute(f'''
            UPDATE users SET {', '.join(fields)}, updated_at = ?
            WHERE user_id = ?
        ''', vals)
    c.execute('''
        INSERT INTO user_log (user_id, weight, hips, thigh, waist, chest, biceps, logged_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        kwargs.get('weight'),
        kwargs.get('hips'),
        kwargs.get('thigh'),
        kwargs.get('waist'),
        kwargs.get('chest'),
        kwargs.get('biceps'),
        now
    ))
    conn.commit(); conn.close()

def get_user_progress_for_periods(user_id, param):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    now = datetime.now()
    c.execute(f'''
        SELECT {param}, logged_at
        FROM user_log
        WHERE user_id = ? AND {param} IS NOT NULL
        ORDER BY logged_at DESC
    ''', (user_id,))
    rows = c.fetchall(); conn.close()
    vals = [(r[0], datetime.fromisoformat(r[1])) for r in rows]
    res = {}
    if not vals:
        msg = 'Нет данных — вы ещё не добавляли измерения'
        return {
            'С последнего измерения': msg,
            'За неделю': {'value': msg, 'date': None},
            'За месяц': {'value': msg, 'date': None},
            'С начала измерений': msg
        }
    res['С последнего измерения'] = (
        str(vals[0][0] - vals[1][0])
        if len(vals) >= 2 else
        'Нет данных для сравнения'
    )
    for label, days in [('За неделю',7),('За месяц',30)]:
        cur_v, cur_d = vals[0]
        cutoff = (now - timedelta(days=days)).date()
        past = [(v,d) for v,d in vals if d.date() <= cutoff]
        if past:
            v,d = past[-1]
            res[label] = {'value': str(cur_v-v), 'date': d.strftime('%d.%m.%Y')}
        else:
            ld = cur_d.strftime('%d.%m.%Y')
            if (now.date() - cur_d.date()).days < days:
                res[label] = {'value': f'нет данных — не прошло {days} дней', 'date': ld}
            else:
                res[label] = {'value': 'нет данных за период', 'date': ld}
    res['С начала измерений'] = (
        str(vals[0][0] - vals[-1][0])
        if len(vals) >= 2 else
        'нет данных для сравнения с началом'
    )
    return res
