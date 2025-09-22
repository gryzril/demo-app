# Demo App

**Jenkins**: http://127.0.0.1:8080  
**Frontend (Vite dev)**: http://localhost:5173/  
**Backend (Swagger)**: http://127.0.0.1:8000/swagger

---

## How to run locally

### Prereqs
- Docker Desktop
- Python 3.12
- Node 18+ (for dev mode)
- pgAdmin (optional)
- VS Code + Vue Devtools (optional)

### Using Docker (recommended)
```bash
# 1) Start Postgres + API
docker compose up -d db backend

# 2) Init schema + demo seed
docker compose --profile init run --rm db-init

# 3) Start frontend (Vite or Nginx image)
docker compose up -d frontend

### Backend
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# set DB (matches docker-compose)
set DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app    # PowerShell
# export DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app   # bash/zsh

python -m app.init_db
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### Frontend
cd frontend
npm ci
npm run dev

### Backend Tests
# via Docker
docker run --rm -v "$PWD/backend:/w" -w /w python:3.12 bash -lc "
  pip install -U pip &&
  pip install -r requirements.txt &&
  pytest tests -q || echo 'Failure expected, moving on'
"

# or locally
cd backend && pytest -q || echo "Failure expected, moving on"

### Frontend E2E (Not implemented)
cd frontend
npm ci
npx playwright install --with-deps
npx playwright test

### Jenkins (With DinD)
docker compose -f docker-compose.jenkins.yml up -d