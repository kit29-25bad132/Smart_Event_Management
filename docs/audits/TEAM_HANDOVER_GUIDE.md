# Team Handover Guide

## Read first

Read `FINAL_AUDIT_SUMMARY.md`, then this guide, `PHASE_3_TO_FINAL_IMPLEMENTATION_PLAN.md`, and the existing `docs/backend/phase2-wsl-validation.md`.

## Request flow

`Client → FastAPI router → dependencies/authentication → service → SQLAlchemy session → PostgreSQL → response`.

- App registration and handlers: `backend/app/main.py`.
- Routers: `backend/app/api/`.
- Identity and role checks: `backend/app/core/dependencies.py`, `security.py`.
- Domain rules and commits: `backend/app/services/`.
- Models/session: `backend/app/models/`, `backend/app/db/`.
- Request/response contracts: `backend/app/schemas/`.

Keep business rules in services. Routers should translate HTTP contracts and dependencies, not duplicate domain decisions. Future agent tools must call services and must not access tables directly.

## Database and transactions

The initial migration creates users, venues, events and registrations, with UUID keys, foreign keys, enums, uniqueness/indexes and registration/event relationships. Registration locks the event row before counting active registrations. Event creation/update locks the venue row before checking overlapping active events. Ordinary integration tests use a savepoint/outer-rollback fixture; concurrency tests intentionally use independent sessions with real service commits.

Never point integration tests at Supabase. Set `TEST_DATABASE_URL` to the dedicated local endpoint and allow the safety gate to reject anything else. Do not print secrets or complete URLs.

## Local validation

From WSL:

```bash
cd /mnt/c/Users/kit29/Desktop/Smart_Event_Management/backend
export UV_PROJECT_ENVIRONMENT=/home/kit29/.venvs/smart-event-backend
uv sync --locked --extra dev
uv run python -m pytest -v
uv run python -m alembic history
uv run python -m alembic heads
```

For integration tests, configure only the isolated `TEST_DATABASE_URL`. Run migrations only after explicit approval and with a temporary `DATABASE_URL="$TEST_DATABASE_URL"` command override. Full commands and troubleshooting are in `docs/backend/phase2-wsl-validation.md`.

## Adding work safely

- New API route: add schema, router, dependency and service tests; register the router in `main.py`.
- New domain rule: implement it in the service and test both success and standardized errors.
- Schema change: update model, migration, database docs and integration tests together.
- Agent tool: define typed input/output, identity context and confirmation rules; call a service.
- Test: use unique records, isolated DB configuration and guaranteed cleanup; never fall back to `DATABASE_URL`.

## Troubleshooting

Readiness 503 means the configured database is unavailable; inspect only non-secret host/driver metadata. A skipped integration suite means the safety gate rejected missing, non-local, production-like or application-equivalent configuration. Migration failures must be resolved against the isolated database only.
