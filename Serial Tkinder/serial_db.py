"""
serial_db.py
Lógica de base de datos para almacenar lecturas numéricas recibidas por serial.

Estructura de tabla:
- id (INTEGER, PK, autoincrement)
- ts (TEXT, ISO8601)
- port (TEXT)
- baud (INTEGER)
- raw (TEXT)         # línea cruda desde el puerto
- value (REAL)       # valor numérico extraído de la línea (uno por fila)

Uso típico:
    import serial_db as sdb
    sdb.init_db("serial_data.sqlite3")
    n = sdb.insert_from_line(port="COM3", baud=9600, line="T=23.5 H=61.2", db_path="serial_data.sqlite3")
"""

import sqlite3
import re
from datetime import datetime
from typing import Iterable, List, Tuple, Optional

DEFAULT_DB_PATH = "serial_data.sqlite3"

# Expresión regular para números (enteros, decimales, con signo, y notación científica)
NUM_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

def get_conn(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Retorna una conexión SQLite (crea archivo si no existe)."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Crea la tabla si no existe."""
    with get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                ts    TEXT NOT NULL,
                port  TEXT,
                baud  INTEGER,
                raw   TEXT,
                value REAL
            );
            """
        )
        conn.commit()

def extract_numbers(line: str) -> List[float]:
    """Extrae TODOS los números de una línea de texto."""
    return [float(m.group()) for m in NUM_RE.finditer(line)]

def insert_many(
    rows: Iterable[Tuple[str, Optional[str], Optional[int], Optional[str], Optional[float]]],
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Inserta múltiples filas.
    rows: iterable de (ts_iso, port, baud, raw, value)
    Retorna la cantidad insertada.
    """
    with get_conn(db_path) as conn:
        conn.executemany(
            "INSERT INTO readings (ts, port, baud, raw, value) VALUES (?, ?, ?, ?, ?);",
            rows
        )
        conn.commit()
        return conn.total_changes

def insert_from_line(
    port: Optional[str],
    baud: Optional[int],
    line: str,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Extrae números de la línea y crea UNA fila por cada número hallado.
    Retorna cuántas filas se insertaron.
    """
    nums = extract_numbers(line)
    if not nums:
        return 0
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    rows = [(ts, port, baud, line.strip(), v) for v in nums]
    return insert_many(rows, db_path=db_path)

def count(db_path: str = DEFAULT_DB_PATH) -> int:
    """Cuenta total de filas."""
    with get_conn(db_path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM readings;")
        return int(cur.fetchone()[0])

def recent(limit: int = 10, db_path: str = DEFAULT_DB_PATH) -> List[Tuple[int, str, str, int, str, float]]:
    """
    Devuelve las últimas N filas: (id, ts, port, baud, raw, value)
    """
    with get_conn(db_path) as conn:
        cur = conn.execute(
            "SELECT id, ts, port, baud, raw, value FROM readings ORDER BY id DESC LIMIT ?;",
            (limit,)
        )
        return list(cur.fetchall())

def clear(db_path: str = DEFAULT_DB_PATH) -> int:
    """Borra todas las filas (¡cuidado!). Retorna filas afectadas."""
    with get_conn(db_path) as conn:
        cur = conn.execute("DELETE FROM readings;")
        conn.commit()
        return cur.rowcount
