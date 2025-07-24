
import aiosqlite

DB_NAME = "valhalla.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                tg_id INTEGER UNIQUE,
                username TEXT,
                game_nick TEXT,
                game_id TEXT,
                server TEXT,
                roles TEXT,
                status TEXT
            )
        ''')
        await db.commit()

async def add_user(tg_id, username, game_nick, game_id, server, roles):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO users (tg_id, username, game_nick, game_id, server, roles, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tg_id, username, game_nick, game_id, server, ",".join(roles), 'pending'))
        await db.commit()

async def user_exists(tg_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT 1 FROM users WHERE tg_id = ?', (tg_id,))
        return await cursor.fetchone() is not None

async def get_user(tg_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
        return await cursor.fetchone()

async def delete_user(tg_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM users WHERE tg_id = ?', (tg_id,))
        await db.commit()
