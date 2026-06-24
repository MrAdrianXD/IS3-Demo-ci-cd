# Liquidación de Sueldos — Demo CI/CD

Demo para clase de CI/CD: una app simple de **liquidación de sueldos**, dividida en
**backend (FastAPI)** y **frontend (React + Vite)**, con pipelines independientes en
**GitHub Actions** que corren tests/build y despliegan a **Render** (API) y **Netlify** (UI).

## Estructura

```
.
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── liquidacion.py   # Lógica de negocio (clase Liquidacion)
│   │   └── main.py          # Endpoints FastAPI
│   ├── tests/
│   │   ├── test_liquidacion.py        # Tests unitarios
│   │   └── test_api_integration.py    # Tests de integración (TestClient)
│   ├── requirements.txt
│
├── frontend/                 # UI React + Vite
│   └── src/
│       ├── App.jsx
│       └── index.css
```

## Cómo correr localmente

### Backend

Con UV:  
```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Con pip:  
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Tests (habiendo cargado el entorno):

```bash
cd backend
uv run pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # ajustar VITE_API_URL si hace falta
npm run dev
```

## Pipelines de GitHub Actions

## Setup de secrets y variables necesarios

### En GitHub (`Settings → Secrets and variables → Actions`)

| Tipo      | Nombre                  | Dónde se obtiene                                                                 |
|-----------|--------------------------|-----------------------------------------------------------------------------------|
| Secret    | `RENDER_DEPLOY_HOOK_URL` | Render → tu servicio → **Settings → Deploy Hook** (copiar la URL)                |
| Secret    | `NETLIFY_AUTH_TOKEN`     | Netlify → **User settings → Applications → Personal access tokens**              |
| Secret    | `NETLIFY_SITE_ID`        | Netlify → tu sitio → **Site settings → General → Site details → Site ID**        |
| Variable  | `VITE_API_URL`           | URL pública de tu servicio en Render (ej: `https://liquidacion-api.onrender.com`) |

> Los **secrets** son para credenciales; las **variables** (`vars.*`) son para valores no
> sensibles como la URL de la API — sirve para mostrar en clase la diferencia entre ambos.

### En Render
1. Crear un **Web Service** nuevo, conectado al repo (o usando `backend/render.yaml`
   como Blueprint).
2. Root directory: `backend`.
3. Build command: `pip install -r requirements.txt` o `uv sync`.
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` o `uv run`.
5. Copiar el **Deploy Hook** y guardarlo como secret en GitHub.

### En Netlify
1. Crear un sitio nuevo (puede ser "Deploy manually" para no duplicar el auto-deploy,
   ya que el deploy real lo va a hacer Actions).
2. Generar un **Personal Access Token** y copiar el **Site ID** del sitio.
3. Guardar ambos como secrets en GitHub.
