import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "users.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                nickname TEXT,
                role TEXT,
                game_id TEXT,
                server TEXT,
                extra TEXT
            )
        """)
        conn.commit()

def get_user(user_id):
    return get_user_data(user_id)
    
def is_registered(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (str(user_id),))
        return cursor.fetchone() is not None

def register_user(user_id, data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (user_id, nickname, role, game_id, server, extra)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(user_id),
            data.get("nickname"),
            data.get("role"),
            data.get("game_id"),
            data.get("server"),
            data.get("extra", "")
        ))
        conn.commit()

def get_user_data(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row[0],
                "nickname": row[1],
                "role": row[2],
                "game_id": row[3],
                "server": row[4],
                "extra": row[5],
            }
        return None

def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (str(user_id),))
        conn.commit()
        return cursor.rowcount > 0

def get_all_users():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [dict(zip(
            ["user_id", "nickname", "role", "game_id", "server", "extra"], row
        )) for row in rows]
