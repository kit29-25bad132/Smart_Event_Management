# Backend setup

Phase 2 implements the non-AI FastAPI backend. Use Python 3.12/3.13 when available; the repository constraint also permits 3.14. The supported local flow is `uv` or a virtual environment, PostgreSQL, and Alembic migrations.

```powershell
cd backend
uv sync --extra dev
Copy-Item .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

On managed Windows systems that block SQLAlchemy's optional native Cython extensions, use SQLAlchemy's supported pure-Python rebuild path:

```powershell
$env:DISABLE_SQLALCHEMY_CEXT = "1"
uv sync --extra dev --no-binary-package sqlalchemy
```

This does not disable Windows security policy; it installs the same SQLAlchemy version without optional compiled extensions.

