# Phase 2 WSL validation guide

Run from Ubuntu WSL2. Do not print secrets or use the application database for tests or migrations.

## Dependencies and unit tests

```bash
cd /mnt/c/Users/kit29/Desktop/Smart_Event_Management/backend
export UV_PROJECT_ENVIRONMENT=/home/kit29/.venvs/smart-event-backend
export DISABLE_SQLALCHEMY_CEXT=1
uv sync --locked --extra dev --no-binary-package sqlalchemy
uv run python -c 'import fastapi, sqlalchemy, jwt; print("imports ok")'
uv run python -m alembic --version
uv run python -m pytest -v tests/test_configuration.py tests/test_error_contract.py
```

## Safe PostgreSQL test database

Use a dedicated local database only. The integration suite requires `TEST_DATABASE_URL`, rejects missing or identical application URLs, rejects non-local hosts, and never creates or drops databases.

```bash
export TEST_DATABASE_URL='postgresql+psycopg://test_user:test_password@localhost:5432/smart_event_management_test'
psql "$TEST_DATABASE_URL" -c 'SELECT 1;'
```

## Migration inspection and approved execution

```bash
uv run python -m alembic history
uv run python -m alembic heads
# Only after confirming TEST_DATABASE_URL is isolated. This temporary override
# affects only this command and does not edit backend/.env:
DATABASE_URL="$TEST_DATABASE_URL" uv run python -m alembic upgrade head
DATABASE_URL="$TEST_DATABASE_URL" uv run python -m alembic current
```

Expected head/current revision: `0001_initial_schema`.

## Integration tests

```bash
TEST_DATABASE_URL="$TEST_DATABASE_URL" uv run python -m pytest -v tests/test_integration_postgres.py
```

Tests use the pre-migrated schema and roll back each test transaction. Unsafe or missing configuration produces a clear skip reason.

## Application smoke tests

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
curl -i http://127.0.0.1:8000/api/health
curl -i http://127.0.0.1:8000/api/ready
curl -i http://127.0.0.1:8000/docs
curl -i http://127.0.0.1:8000/redoc
```

Health/docs should return 200. Readiness should return 200 with the isolated database and 503 with the standardized error envelope when unavailable.

## Git verification

```bash
git diff --check
git status --short
git diff --stat
git ls-files | grep -E '(^|/)(\.env($|\.)|\.venv|node_modules)' || true
```

Do not stage, commit, or push without review.

## Troubleshooting

- Missing `TEST_DATABASE_URL`: integration tests skip safely.
- `TEST_DATABASE_URL` equals `DATABASE_URL`: the safety gate rejects it.
- Supabase or production-like host: the safety gate rejects it.
- Readiness 503: verify only non-secret host/driver metadata and isolated database credentials.
- Native-extension errors: use WSL2 and retain the SQLAlchemy workaround above.
- Alembic authentication failure: correct only the isolated test configuration; do not substitute production credentials.
