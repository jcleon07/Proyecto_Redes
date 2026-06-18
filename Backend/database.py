import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "crimes.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    #Tabla crimenes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_delito TEXT NOT NULL,
            localidad TEXT NOT NULL,
            barrio TEXT,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)

    #Tabla CAIs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            localidad TEXT NOT NULL,
            latitud REAL NOT NULL,
            longitud REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def seed_cais():
    # Se insertan los CAIs solo si la tabla aún está vacía
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cais")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    cais_data = [
        ("CAI Chapinero",       "Chapinero",      4.6490, -74.0560),
        ("CAI Chicó",           "Chapinero",      4.6610, -74.0530),
        ("CAI La Candelaria",   "Santa Fe",       4.5985, -74.0765),
        ("CAI Kennedy",         "Kennedy",        4.6280, -74.1495),
        ("CAI Patio Bonito",    "Kennedy",        4.6095, -74.1610),
        ("CAI Suba",            "Suba",           4.7420, -74.0840),
        ("CAI Usaquén",         "Usaquén",        4.6960, -74.0315),
        ("CAI Bosa",            "Bosa",           4.6195, -74.1880),
        ("CAI Ciudad Bolívar",  "Ciudad Bolívar", 4.5545, -74.1415),
        ("CAI Engativá",        "Engativá",       4.7055, -74.1105),
    ]

    cursor.executemany("""
        INSERT INTO cais (nombre, localidad, latitud, longitud)
        VALUES (?, ?, ?, ?)
    """, cais_data)

    conn.commit()
    conn.close()
    print("Datos insertados correctamente")