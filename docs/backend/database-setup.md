# Database setup

Set `DATABASE_URL` to a PostgreSQL URL using the `psycopg` driver. Run `uv run alembic upgrade head` to apply `migrations/versions/0001_initial_schema.py`; do not use `Base.metadata.create_all()` in application startup. Readiness executes `SELECT 1` and returns 503 when the database is unavailable.

