
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parents[1] / "data/app.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql: str, params: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    conn.close()
    return result

def query_one(sql: str, params: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchone()
    conn.close()
    return result
