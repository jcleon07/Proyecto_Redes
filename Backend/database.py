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

def seed_db():
    #Se insertan datos ejemplo si la database esta vacia
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM crimes")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    crimes_data = [
        # (tipo_delito, localidad, barrio, latitud, longitud, fecha, hora)
        ("hurto a persona",     "Chapinero",      "Chapinero Alto",   4.6486, -74.0570, "2024-01-10", "22:30"),
        ("hurto a persona",     "Chapinero",      "Chicó",            4.6601, -74.0527, "2024-01-11", "20:15"),
        ("hurto a persona",     "Chapinero",      "Chapinero Alto",   4.6490, -74.0565, "2024-01-15", "21:00"),
        ("hurto a vehículo",    "Chapinero",      "Chicó Norte",      4.6620, -74.0510, "2024-01-12", "03:00"),
        ("hurto a persona",     "Santa Fe",       "La Candelaria",    4.5981, -74.0760, "2024-01-10", "13:00"),
        ("hurto a persona",     "Santa Fe",       "La Candelaria",    4.5975, -74.0755, "2024-01-18", "14:30"),
        ("lesiones personales", "Santa Fe",       "San Victorino",    4.6012, -74.0810, "2024-01-20", "23:00"),
        ("hurto a persona",     "Kennedy",        "Patio Bonito",     4.6100, -74.1600, "2024-01-13", "19:45"),
        ("hurto a persona",     "Kennedy",        "Tintal",           4.6080, -74.1700, "2024-01-14", "20:00"),
        ("hurto a vehículo",    "Kennedy",        "Kennedy Central",  4.6278, -74.1490, "2024-01-16", "02:30"),
        ("hurto a vehículo",    "Kennedy",        "Patio Bonito",     4.6090, -74.1620, "2024-01-22", "01:00"),
        ("lesiones personales", "Kennedy",        "Kennedy Central",  4.6270, -74.1480, "2024-01-25", "23:45"),
        ("hurto a persona",     "Suba",           "Suba Centro",      4.7416, -74.0837, "2024-01-17", "21:30"),
        ("hurto a persona",     "Suba",           "Lisboa",           4.7500, -74.0900, "2024-01-19", "22:00"),
        ("hurto a vehículo",    "Suba",           "Niza",             4.7200, -74.0780, "2024-01-21", "03:15"),
        ("hurto a persona",     "Usaquén",        "Santa Bárbara",    4.6970, -74.0310, "2024-01-23", "20:45"),
        ("hurto a persona",     "Usaquén",        "Usaquén Centro",   4.6950, -74.0320, "2024-01-24", "19:30"),
        ("hurto a vehículo",    "Usaquén",        "Country Club",     4.6860, -74.0350, "2024-01-26", "02:00"),
        ("hurto a persona",     "Bosa",           "Bosa Centro",      4.6191, -74.1884, "2024-01-27", "21:00"),
        ("hurto a persona",     "Bosa",           "El Porvenir",      4.6150, -74.1900, "2024-01-28", "20:30"),
        ("lesiones personales", "Ciudad Bolívar", "Lucero",           4.5540, -74.1420, "2024-01-29", "22:00"),
        ("hurto a persona",     "Ciudad Bolívar", "Perdomo",          4.5600, -74.1500, "2024-01-30", "21:15"),
        ("hurto a persona",     "Engativá",       "Quirigua",         4.7050, -74.1100, "2024-02-01", "20:00"),
        ("hurto a vehículo",    "Engativá",       "Bolivia",          4.7100, -74.1200, "2024-02-02", "03:30"),
        ("hurto a persona",     "Teusaquillo",    "Galerías",         4.6470, -74.0830, "2024-02-03", "21:45"),
        ("hurto a persona",     "Teusaquillo",    "Chapinero",        4.6500, -74.0800, "2024-02-04", "22:15"),
        ("lesiones personales", "Los Mártires",   "Voto Nacional",    4.6130, -74.0900, "2024-02-05", "23:30"),
        ("hurto a persona",     "Los Mártires",   "La Favorita",      4.6100, -74.0920, "2024-02-06", "20:45"),
        ("hurto a persona",     "Fontibón",       "Fontibón Centro",  4.6700, -74.1450, "2024-02-07", "21:00"),
        ("hurto a vehículo",    "Fontibón",       "Modelia",          4.6650, -74.1300, "2024-02-08", "02:45"),
    ]

    cursor.executemany("""
        INSERT INTO crimes (tipo_delito, localidad, barrio, latitud, longitud, fecha, hora)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, crimes_data)

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