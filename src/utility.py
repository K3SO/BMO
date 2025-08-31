import sqlite3

def db_execute(query: str, params: tuple = (), fetchone=False, fetchall=False):
    with sqlite3.connect(f'bmo_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        conn.commit()

def ensure_user_exists(user_id, user_name: str):
    db_execute(
        'INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)',
        (user_id, user_name)
    )