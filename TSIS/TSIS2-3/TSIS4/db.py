import psycopg2
from config import load_config


def connect():
    return psycopg2.connect(**load_config())


def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
        """
    ]

    with connect() as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)


def get_or_create_player(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO players(username)
                VALUES (%s)
                ON CONFLICT (username) DO NOTHING;
            """, (username,))

            cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
            return cur.fetchone()[0]


def save_game_result(username, score, level):
    player_id = get_or_create_player(username)

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions(player_id, score, level_reached)
                VALUES (%s, %s, %s);
            """, (player_id, score, level))


def get_personal_best(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                WHERE p.username = %s;
            """, (username,))

            return cur.fetchone()[0]


def get_top_10():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC
                LIMIT 10;
            """)

            return cur.fetchall()