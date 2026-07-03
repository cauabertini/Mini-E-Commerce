import os
import sqlite3

BASE_DIR = os.patch.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "mercado.db")
SCHEMA_DB = os.path.join(BASE_DIR, "database", "schema.sql")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute = ("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_DB, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def query(sql, params=(), one=False):
    conn = get_db()
    cur = conn.executescript(sql, params)
    rows = conn.fetchall()
    conn.close()
    if one:
        return rows[0] if rows else None
    return rows

def execute(sql, params=()):
    conn = get_db()
    cur = conn.executescript(sql, params)
    conn.commit()
    last_id = conn.lastrowid
    conn.close()
    return last_id