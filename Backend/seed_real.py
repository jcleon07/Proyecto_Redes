import sqlite3
import random
import os
from datetime import date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "crimes.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Basado en datos reales SIEDCO / Informe Anual Seguridad Bogotá 2024
# Fuentes: Concejo de Bogotá, Probogotá, Secretaría de Seguridad

LOCALIDADES = {
    # (nombre, lat_centro, lng_centro, radio_aprox, peso_relativo)
    "Suba":           (4.7416, -74.0837, 0.040, 14),
    "Engativá":       (4.7050, -74.1100, 0.030, 11),
    "Kennedy":        (4.6278, -74.1490, 0.035, 10),
    "Chapinero":      (4.6601, -74.0527, 0.025,  9),
    "Los Mártires":   (4.6130, -74.0900, 0.015,  8),
    "Santa Fe":       (4.5981, -74.0760, 0.020,  8),
    "Ciudad Bolívar": (4.5540, -74.1420, 0.035,  7),
    "Bosa":           (4.6191, -74.1884, 0.030,  6),
    "Usaquén":        (4.6970, -74.0310, 0.030,  5),
    "Teusaquillo":    (4.6470, -74.0830, 0.020,  5),
    "Fontibón":       (4.6700, -74.1450, 0.025,  4),
    "Rafael Uribe":   (4.5700, -74.1100, 0.025,  5),
    "Puente Aranda":  (4.6250, -74.1050, 0.020,  4),
    "Barrios Unidos": (4.6700, -74.0870, 0.020,  3),
    "Tunjuelito":     (4.5780, -74.1300, 0.020,  3),
    "Usme":           (4.4800, -74.1300, 0.040,  3),
    "San Cristóbal":  (4.5600, -74.0850, 0.025,  4),
    "La Candelaria":  (4.5975, -74.0755, 0.010,  3),
    "Antonio Nariño": (4.5940, -74.1080, 0.015,  2),
    "Mártires":       (4.6100, -74.0920, 0.015,  3),
}

BARRIOS_POR_LOCALIDAD = {
    "Suba":           ["Suba Centro","Lisboa","Niza","Tibabuyes","La Gaitana","El Rincón","Britalia"],
    "Engativá":       ["Quirigua","Bolivia","Minuto de Dios","Boyacá Real","Garcés Navas"],
    "Kennedy":        ["Kennedy Central","Patio Bonito","Tintal","Castilla","Américas","Corabastos"],
    "Chapinero":      ["Chapinero Alto","Chicó","Chicó Norte","Cabrera","Rosales"],
    "Los Mártires":   ["Voto Nacional","La Favorita","Eduardo Santos","Santa Isabel"],
    "Santa Fe":       ["La Candelaria","San Victorino","El Dorado","Las Cruces"],
    "Ciudad Bolívar": ["Lucero","Perdomo","El Tesoro","Ismael Perdomo","Arborizadora"],
    "Bosa":           ["Bosa Centro","El Porvenir","Bosa Occidental","San Bernardino"],
    "Usaquén":        ["Santa Bárbara","Usaquén Centro","Country Club","Cedritos","La Uribe"],
    "Teusaquillo":    ["Galerías","Palermo","Soledad","La Esmeralda","Quinta Paredes"],
    "Fontibón":       ["Fontibón Centro","Modelia","Capellanía","Zona Franca"],
    "Rafael Uribe":   ["Marco Fidel Suárez","Diana Turbay","Marruecos","Quiroga"],
    "Puente Aranda":  ["Puente Aranda","Muzú","Zona Industrial","Ciudad Montes"],
    "Barrios Unidos": ["Doce de Octubre","Andes","Alcázares","Polo Club"],
    "Tunjuelito":     ["Tunjuelito","Abraham Lincoln","Venecia","San Benito"],
    "Usme":           ["Usme Centro","Gran Yomasa","Alfonso López","Comuneros"],
    "San Cristóbal":  ["San Cristóbal","20 de Julio","La Gloria","La Victoria"],
    "La Candelaria":  ["La Candelaria","Egipto","Centro Histórico","Las Aguas"],
    "Antonio Nariño": ["Antonio Nariño","Restrepo","Ciudad Jardín Sur"],
    "Mártires":       ["Voto Nacional","La Favorita","Ricaurte","Santa Isabel"],
}

# Tipos de delito con pesos basados en proporciones reales 2024
# hurto a personas: ~130.000 casos -> mayor volumen
# violencia intrafamiliar: ~42.372
# lesiones personales: relevante
# homicidio: ~1.206
# hurto a vehículo: ~6.000
# hurto a residencia: ~6.036
# extorsión: ~2.497
# delitos sexuales: ~9.107
TIPOS_DELITO = [
    ("hurto a persona",        38),
    ("violencia intrafamiliar", 16),
    ("lesiones personales",     14),
    ("hurto a residencia",      10),
    ("delito sexual",            8),
    ("hurto a vehículo",         7),
    ("extorsión",                4),
    ("homicidio",                2),
    ("hurto a comercio",         1),
]

# Franjas horarias con pesos reales (noche y madrugada concentran más crímenes)
FRANJAS = [
    (( 0,  5), 18),  # madrugada — hurtos a residencia, homicidios
    (( 6, 11),  8),  # mañana
    ((12, 17), 14),  # tarde
    ((18, 23), 60),  # noche — mayor concentración según SIEDCO
]

def fecha_aleatoria():
    inicio = date(2024, 1, 1)
    fin    = date(2024, 12, 31)
    return inicio + timedelta(days=random.randint(0, (fin - inicio).days))

def hora_aleatoria():
    pesos  = [f[1] for f in FRANJAS]
    franja = random.choices(FRANJAS, weights=pesos, k=1)[0]
    hora   = random.randint(franja[0][0], franja[0][1])
    minuto = random.randint(0, 59)
    return f"{hora:02d}:{minuto:02d}"

def coord_aleatoria(lat_c, lng_c, radio):
    lat = lat_c + random.uniform(-radio, radio)
    lng = lng_c + random.uniform(-radio, radio)
    return round(lat, 5), round(lng, 5)

def generar_crimes(n=300):
    nombres_loc = list(LOCALIDADES.keys())
    pesos_loc   = [LOCALIDADES[l][3] for l in nombres_loc]
    pesos_tipo  = [t[1] for t in TIPOS_DELITO]

    crimes = []
    for _ in range(n):
        localidad = random.choices(nombres_loc, weights=pesos_loc, k=1)[0]
        lat_c, lng_c, radio, _ = LOCALIDADES[localidad]
        tipo = random.choices(TIPOS_DELITO, weights=pesos_tipo, k=1)[0][0]
        barrio = random.choice(BARRIOS_POR_LOCALIDAD.get(localidad, ["Centro"]))
        lat, lng = coord_aleatoria(lat_c, lng_c, radio)
        fecha = fecha_aleatoria().isoformat()
        hora  = hora_aleatoria()

        # Ajustes realistas por tipo:
        # homicidios más concentrados en Ciudad Bolívar, Kennedy, Rafael Uribe
        if tipo == "homicidio":
            localidad = random.choices(
                ["Ciudad Bolívar","Kennedy","Rafael Uribe","Suba","Santa Fe"],
                weights=[30,25,20,15,10], k=1
            )[0]
            lat_c, lng_c, radio, _ = LOCALIDADES[localidad]
            lat, lng = coord_aleatoria(lat_c, lng_c, radio)
            barrio = random.choice(BARRIOS_POR_LOCALIDAD[localidad])

        # Hurto a residencia más frecuente en madrugada
        if tipo == "hurto a residencia":
            hora = f"{random.randint(0,5):02d}:{random.randint(0,59):02d}"

        crimes.append((tipo, localidad, barrio, lat, lng, fecha, hora))

    return crimes

def seed_real():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM crimes")
    existing = cursor.fetchone()[0]
    if existing > 30:
        print(f"Ya existen {existing} registros. Limpiando para insertar dataset real...")
        cursor.execute("DELETE FROM crimes")
        conn.commit()

    crimes = generar_crimes(100000)
    cursor.executemany("""
        INSERT INTO crimes (tipo_delito, localidad, barrio, latitud, longitud, fecha, hora)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, crimes)
    conn.commit()
    print(f"{len(crimes)} crímenes insertados basados en datos reales de Bogotá 2024.")

    # Verificar distribución
    cursor.execute("SELECT tipo_delito, COUNT(*) as c FROM crimes GROUP BY tipo_delito ORDER BY c DESC")
    print("\nDistribución por tipo:")
    for row in cursor.fetchall():
        print(f"  {row[0]:<25} {row[1]} casos")

    cursor.execute("SELECT localidad, COUNT(*) as c FROM crimes GROUP BY localidad ORDER BY c DESC LIMIT 5")
    print("\nTop 5 localidades:")
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} {row[1]} casos")

    conn.close()

if __name__ == "__main__":
    seed_real()