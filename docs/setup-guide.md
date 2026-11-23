# Local setup

Use Windows PowerShell for the frontend and repository tasks. Use Ubuntu WSL2 for backend validation when the Linux virtual environment is the supported project environment.

## Backend — Windows PowerShell

```powershell
cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
python -c "import fastapi, sqlalchemy, alembic, jwt; print('backend imports: PASS')"
python -m pytest -v
uvicorn app.main:app --reload --port 8000
```

`/api/ready` requires a reachable development PostgreSQL database configured in `backend/.env`; `/api/health` and `/docs` do not. Never copy production credentials into examples or tests.

## Backend — Ubuntu WSL2

```bash
cd /mnt/c/Users/kit29/Desktop/Smart_Event_Management/backend
export UV_PROJECT_ENVIRONMENT=/home/kit29/.venvs/smart-event-backend
uv sync --locked --extra dev
uv run python -c 'import fastapi, sqlalchemy, alembic, jwt; print("backend imports: PASS")'
uv run python -m pytest -v
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use the isolated PostgreSQL instructions in `docs/backend/phase2-wsl-validation.md` for integration tests. Do not run migrations or destructive tests against Supabase without explicit approval.

## Frontend

In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run typecheck
npm run build
npm run dev
```

Open `http://localhost:3000`. API checks: `http://localhost:8000/api/health` and `/api/ready`.

The frontend uses `NEXT_PUBLIC_API_URL` from `frontend/.env.local`. If a Windows production build reports `spawn EPERM`, repeat the build in WSL or a permitted local CI environment; do not weaken the build configuration to hide the failure.
