# Proyecto Redes UNAL 2026-1S

Este proyecto consiste en una API backend para consultar información sobre criminalidad en Bogotá y un frontend estático que muestra un mapa interactivo con filtros y estadísticas.

## Estructura del proyecto

- `Backend/`: API desarrollada con FastAPI y base de datos SQLite.
- `Frontend/`: interfaz web con HTML, CSS y JavaScript.

## Requisitos previos

- Python 3.10 o superior
- Un navegador web

## Cómo ejecutar el Backend

1. Entrar a la carpeta del backend:
   ```bash
   cd Backend
   ```

2. Crear un entorno virtual:
   ```bash
   python -m venv .venv
   ```

3. Activar el entorno virtual:
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Iniciar la API:
   ```bash
   uvicorn main:app --reload
   ```

6. La API quedará disponible en:
   - http://127.0.0.1:8000

> La primera vez que se ejecute, el backend creará la base de datos SQLite y llenará datos de ejemplo automáticamente.

## Cómo ejecutar el Frontend

Existen dos formas sencillas de abrir la interfaz:

### Opción 1: abrir el archivo directamente

1. Abre el archivo `Frontend/index.html` en tu navegador.
2. Asegúrate de que el backend esté corriendo antes de usar la interfaz.

### Opción 2: usar un servidor simple

1. Entrar a la carpeta del frontend:
   ```bash
   cd Frontend
   ```

2. Iniciar un servidor local:
   ```bash
   python -m http.server 8080
   ```

3. Abrir en el navegador:
   - http://localhost:8080

## Verificación rápida

Una vez que el backend y el frontend estén corriendo:

- La API debe responder en http://127.0.0.1:8000
- El mapa del frontend debe cargar los datos desde la API
- Si se desea revisar los endpoints disponibles, la documentación en http://127.0.0.1:8000/docs es muy útil

## Notas importantes

- El frontend está configurado para consumir la API en:
  ```text
  http://127.0.0.1:8000
  ```
- Si se cambia la URL del backend, también se debe actualizar la variable `API` dentro de [Frontend/index.html](Frontend/index.html).

