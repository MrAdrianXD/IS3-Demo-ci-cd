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
│   └── render.yaml          # Definición declarativa del servicio en Render
│
├── frontend/                 # UI React + Vite
│   └── src/
│       ├── App.jsx
│       └── index.css
│
├── netlify.toml              # Config de build para Netlify
│
└── .github/workflows/
    ├── backend.yml           # CI/CD del backend → Render
    └── frontend.yml          # CI/CD del frontend → Netlify
```

## Cómo correr localmente

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Tests:

```bash
cd backend
pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # ajustar VITE_API_URL si hace falta
npm run dev
```

## Pipelines de GitHub Actions

Hay **dos workflows independientes**, cada uno disparado solo por cambios en su carpeta
(usando `paths:`), para simular dos equipos/servicios que se despliegan por separado.

### `backend.yml`
1. **test**: instala dependencias y corre `pytest` (unitarios + integración).
2. **deploy** (solo en push a `main`, y solo si los tests pasan): dispara un
   **Deploy Hook** de Render vía `curl`.

### `frontend.yml`
1. **build**: instala dependencias, corre `lint`, y hace `npm run build`.
2. **deploy** (solo en push a `main`): vuelve a buildear con la URL de producción de la
   API y publica el resultado en Netlify usando la action `nwtgck/actions-netlify`.

> **Por qué disparar el deploy desde Actions y no usar el auto-deploy nativo de
> Render/Netlify:** ambas plataformas pueden auto-deployar al conectar el repo
> directamente, pero eso dejaría a GitHub Actions corriendo solo los tests, sin mostrar
> el "CD" del pipeline. Para la demo es más ilustrativo que el propio workflow sea quien
> dispara el deploy.

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
3. Build command: `pip install -r requirements.txt`.
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Copiar el **Deploy Hook** y guardarlo como secret en GitHub.

### En Netlify
1. Crear un sitio nuevo (puede ser "Deploy manually" para no duplicar el auto-deploy,
   ya que el deploy real lo va a hacer Actions).
2. Generar un **Personal Access Token** y copiar el **Site ID** del sitio.
3. Guardar ambos como secrets en GitHub.

## Qué mostrar en la clase

1. Hacer un cambio en `backend/app/liquidacion.py` (ej: romper un cálculo a propósito)
   y ver cómo el job `test` falla y el deploy **no** se ejecuta.
2. Corregirlo, hacer push, y mostrar el pipeline completo: test → deploy → API
   actualizada en Render.
3. Repetir lo mismo con un cambio visual en `frontend/src/App.jsx`, mostrando el segundo
   pipeline corriendo en paralelo e independiente del primero.
4. Mostrar cómo los `paths:` en cada workflow evitan que un cambio en frontend dispare
   el pipeline de backend (y viceversa).
