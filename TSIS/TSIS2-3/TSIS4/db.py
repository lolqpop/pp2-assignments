import psycopg2
from psycopg2 import pool
from config import load_config

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = pool.SimpleConnectionPool(1, 10, **load_config())
    return _pool

def connect():
    return get_pool().getconn()

def release(conn):
    get_pool().putconn(conn)

def execute(query, params=(), fetch=None):
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch == "one": return cur.fetchone()
            if fetch == "all": return cur.fetchall()
    finally:
        release(conn)

def create_tables():
    execute("""CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL)""")
    execute("""CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY, player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL, level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW())""")

def get_or_create_player(username):
    execute("INSERT INTO players(username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    return execute("SELECT id FROM players WHERE username = %s", (username,), fetch="one")[0]

def save_game_result(username, score, level):
    pid = get_or_create_player(username)
    execute("INSERT INTO game_sessions(player_id,score,level_reached) VALUES(%s,%s,%s)", (pid,score,level))

def get_personal_best(username):
    row = execute("""
        SELECT COALESCE(MAX(gs.score),0) FROM game_sessions gs
        JOIN players p ON gs.player_id=p.id WHERE p.username=%s
    """, (username,), fetch="one")
    return row[0]

def get_top_10():
    return execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs JOIN players p ON gs.player_id=p.id
        ORDER BY gs.score DESC LIMIT 10
    """, fetch="all")