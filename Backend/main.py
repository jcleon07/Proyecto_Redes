from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, init_db, seed_db
from typing import Optional

app = FastAPI(title="API Criminalidad Bogota")

#El CORS permite que el Frontend llame al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    seed_db()


# ------------- CRIMENES --------------

@app.get("/crimes")
def get_crimes(
    tipo_delito: Optional[str] = Query(None, description="Filtrar por tipo de delito"),
    localidad: Optional[str] = Query(None, description="Filtrar por localidad"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
):
    #Se devuelve la lista de crimenes con filtros (opcionales)
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM crimes WHERE 1=1"
    params = []

    if tipo_delito:
        query += " AND tipo_delito = ?"
        params.append(tipo_delito)
    if localidad:
        query += " AND localidad = ?"
        params.append(localidad)
    if fecha_inicio:
        query += " AND fecha >= ?"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND fecha <= ?"
        params.append(fecha_fin)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/crimes/heatmap")
def get_heatmap_data(
    tipo_delito: Optional[str] = Query(None),
    localidad: Optional[str] = Query(None)
):
    #Devuelve coordenadas para el mapa de calor (latitud, longitud e intensidad)
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT latitud, longitud FROM crimes WHERE 1=1"
    params = []

    if tipo_delito:
        query += " AND tipo_delito = ?"
        params.append(tipo_delito)
    if localidad:
        query += " AND localidad = ?"
        params.append(localidad)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [[row["latitud"], row["longitud"], 1.0] for row in rows]


@app.get("/crimes/stats")
def get_stats():
    "Estadisticas generales"
    conn = get_connection()
    cursor = conn.cursor()

    #Total crimenes
    cursor.execute("SELECT COUNT(*) as total FROM crimes")
    total = cursor.fetchone()["total"]

    #Por tipo de delito
    cursor.execute("""
    SELECT tipo_delito, COUNT(*) as cantidad
    FROM crimes GROUP BY tipo_delito ORDER BY cantidad DESC
    """)
    por_tipo = [dict(r) for r in cursor.fetchall()]

    #Por localidad
    cursor.execute("""
        SELECT localidad, COUNT(*) as cantidad
        FROM crimes GROUP BY localidad ORDER BY cantidad DESC
    """)
    por_localidad = [dict(r) for r in cursor.fetchall()]

    #Por franja horaria
    cursor.execute("""
        SELECT
            CASE
                WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 0 AND 5 THEN  'Madrugada (0-5h)'
                WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 6 AND 11 THEN  'Mañana (6-11h)'
                WHEN CAST(substr(hora, 1, 2) AS INTEGER) BETWEEN 12 AND 17 THEN  'Tarde (12-17h)'
                ELSE 'Noche (18-23h)'
            END as franja,
            COUNT(*) as cantidad
        FROM crimes GROUP BY franja ORDER BY cantidad DESC
    """)
    por_hora = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total": total,
        "por_tipo": por_tipo,
        "por_localidad": por_localidad,
        "por_hora": por_hora
    }


@app.post("/crimes")
def add_crime(crime:dict):
    #Agregar nuevo crimen a la database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO crimes (tipo_delito, localidad, barrio, latitud, longitud, fecha, hora)
        VALUES (:tipo_delito, :localidad, :barrio, :latitud, :longitud, :fecha, :hora)
    """, crime)
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"message": "Crimen agregado", "id": new_id}


# ------------ CAIs -------------

@app.get("/cais")
def get_cais(localidad: Optional[str] = Query(None)):
    #Devuelve los CAIs  con filtro opcional por localidad
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM cais WHERE 1=1"
    params = []

    if localidad:
        query += " AND localidad = ?"
        params.append(localidad)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ------------ UTIL --------------

@app.get("/localidades")
def get_localidades():
    #Devuelve la lista de localidades disponibles
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT localidad FROM crimes ORDER BY localidad")
    rows = cursor.fetchall()
    conn.close()
    return [row["localidad"] for row in rows]


@app.get("/tipos-delito")
def get_tipos_delito():
    #Devuelve tipos de delito 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT tipo_delito FROM crimes ORDER BY tipo_delito")
    rows = cursor.fetchall()
    conn.close()
    return [row["tipo_delito"] for row in rows]