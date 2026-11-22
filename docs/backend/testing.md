# Testing

Use an isolated PostgreSQL test database and never point tests at production:

```powershell
uv run pytest
uv run alembic upgrade head
```

Tests cover authentication, RBAC, event/venue/registration rules, migration upgrade/downgrade and concurrency. Phase 2 completion requires actual execution evidence; unavailable PostgreSQL credentials are an unresolved environment issue, not a passing test result.
