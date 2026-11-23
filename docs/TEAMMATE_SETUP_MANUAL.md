# Teammate Setup Manual — Agentic AI Smart Event Management System

**Project:** Infosys Agentic AI Smart Event Management System  
**Audience:** New contributors using Windows 10/11 and Visual Studio Code  
**Baseline:** Phases 0–2 formally verified; Phase 3 onward is upcoming work  
**Repository destination:** `docs/TEAMMATE_SETUP_MANUAL.md`

> **Owner action before distribution:** Push the reviewed Phase 0–2 commit, share the actual repository URL and team permissions, and rotate the previously exposed isolated-test database credential. Do not distribute credentials in this document.

## 1. What to install before starting

| Software | Required? | Why | How to check |
|---|---|---|---|
| Git | Yes | Clone, branch, commit, push | `git --version` |
| Visual Studio Code | Yes | Editor and terminal | Launch VS Code |
| VS Code WSL extension | Recommended | Edit and run the Linux workspace | Extensions → WSL |
| WSL 2 with Ubuntu | Recommended Windows setup | Consistent Linux backend environment | PowerShell: `wsl --status`; Ubuntu: `uname -a` |
| Python | Yes, inside Ubuntu | Backend runtime | `python3 --version` |
| `uv` | Yes, inside Ubuntu | Python dependencies and virtual environments | `uv --version` |
| Node.js and npm | Yes, preferably Linux-native inside Ubuntu | Next.js frontend | `node --version`; `npm --version`; `which node` |
| Docker Desktop with WSL integration **or** Docker Engine | For local integration tests | Isolated PostgreSQL 16 | `docker version`; `docker compose version` |
| PostgreSQL client (`psql`) | Optional | Inspect local test DB | `psql --version` |
| GitHub access | Yes, if hosted on GitHub | Repository and pull requests | Confirm invitation and access |

**Do not assume exact Python/Node versions.** Check `backend/pyproject.toml`, `backend/.python-version` if present, and `frontend/package.json` / lockfiles for the project's actual constraints. The owner's verified WSL environment used Python 3.14.4, but teammates should follow the committed project requirements.

## 2. Prepare Windows, Ubuntu, and VS Code

1. Install Git and VS Code on Windows.
2. In **Windows PowerShell as Administrator**, install WSL if not already installed:

   ```powershell
   wsl --install -d Ubuntu
   ```

   Restart Windows if prompted. Existing Ubuntu users should **not** reinstall or unregister their distribution.
3. Open Ubuntu, finish creating your Linux username, then run:

   ```bash
   sudo apt update
   sudo apt install -y curl ca-certificates git build-essential python3 python3-venv
   ```

4. Install `uv` using the official instructions at https://docs.astral.sh/uv/getting-started/installation/ and reopen the terminal. Verify `uv --version`.
5. Install a supported **Linux-native** Node.js version using your team's agreed version manager. Verify both `node` and `npm` inside Ubuntu. Avoid accidentally running Windows npm from WSL.
6. Install Docker Desktop, enable its **WSL integration for Ubuntu**, and verify `docker version` inside Ubuntu. Alternatively use a team-approved Linux Docker Engine.
7. Install the VS Code **WSL** extension. From Ubuntu, open the repository using `code .` after cloning.

## 3. Get access and clone the repository

Ask the project owner for:

- The **actual Git repository clone URL** and permission to access it.
- Your assigned Phase 3–8 task and branch naming convention.
- The approved environment-variable **names** and a safe channel for any required development credentials.
- The approved LLM/embedding provider decision when Phase 3 provider-dependent work begins (ADR-009 is deferred until then).

In Ubuntu:

```bash
mkdir -p ~/projects
cd ~/projects
git clone <ACTUAL_REPOSITORY_URL> Smart_Event_Management
cd Smart_Event_Management
git status
git branch --show-current
code .
```

**Recommendation:** Clone under `~/projects` in the Linux filesystem for more reliable WSL performance. The original owner's Windows-mounted path is not portable and must not be copied verbatim.

Read these project documents before editing code (use the exact paths present in the cloned repository):

1. `README.md` and `docs/setup-guide.md`.
2. `docs/audits/PHASE_0_COMPLETION_REPORT.md`, `PHASE_1_COMPLETION_REPORT.md`, `PHASE_2_COMPLETION_REPORT.md`.
3. `docs/audits/REQUIREMENTS_TRACEABILITY_MATRIX.md`.
4. `docs/architecture/architecture-decisions.md` and `docs/architecture/api-contract-decision-record.md`.
5. `docs/backend/phase2-wsl-validation.md` and `docs/audits/TEAM_HANDOVER_GUIDE.md`, if present.
6. The official Infosys project roadmap supplied by the owner.

## 4. Configure and verify the backend

From Ubuntu in the cloned project:

```bash
cd ~/projects/Smart_Event_Management/backend
uv sync --locked --extra dev
uv run python --version
uv run python -m pytest -v
```

**Expected result without a test DB:** 6 passing non-database tests and 12 skipped PostgreSQL integration tests. This is a valid initial environment smoke check, **not** complete backend verification.

The owner used a separate WSL virtual environment because of filesystem constraints. Teammates using a Linux-native clone should generally let `uv` create its normal project environment. If the project documentation requires an external environment, configure `UV_PROJECT_ENVIRONMENT` as instructed there.

### Environment variables

Inspect the committed configuration examples and backend settings for the actual required variable names. Typical project-specific values include the application database URL and JWT secret. **Do not invent settings or copy the owner's private `.env`.**

- Create a local `.env` only if the repository's setup guide requires it.
- Use a long, randomly generated local JWT secret, not a placeholder.
- Keep `.env`, tokens, database URLs and passwords out of Git and screenshots.
- Do **not** use production or Supabase credentials for local automated tests.
- Verify the ignored status of secret files before committing.

### Start the API

After the required application environment variables and database connection are configured:

```bash
uv run uvicorn app.main:app --host 127.0.0.1 --port 8001
```

In another Ubuntu terminal:

```bash
curl -i http://127.0.0.1:8001/api/health
curl -i http://127.0.0.1:8001/api/ready
curl -sS -o /dev/null -w 'OpenAPI HTTP %{http_code}\n' http://127.0.0.1:8001/openapi.json
```

**Expected:** HTTP 200 for all three when the application and its configured database are ready. `/api/health` should report `healthy`; `/api/ready` should report `ready`. OpenAPI is available at `/openapi.json`.

If `/api/ready` fails, check whether the **application** database is reachable. Do not change a shared database to make readiness pass.

## 5. Set up a dedicated PostgreSQL 16 test database

**Required for full 18-test verification.** Each teammate should use their **own local isolated** PostgreSQL instance/database. Never point `TEST_DATABASE_URL` at Supabase, production, or another person's development database.

If the repository contains a documented Docker Compose setup, prefer that. Otherwise, the following is an example of a **local-only** PostgreSQL container; confirm port `5434` is free before use.

In Ubuntu, enter a new password without echoing it:

```bash
read -rsp 'New local test DB password: ' TEST_DB_PASSWORD; echo
export TEST_DB_PASSWORD
```

Create the container **only if you do not already have a project test container**:

```bash
docker run -d \
  --name smart-event-postgres-test \
  -e POSTGRES_USER=smart_event_test \
  -e POSTGRES_DB=smart_event_management_test \
  -e POSTGRES_PASSWORD="$TEST_DB_PASSWORD" \
  -p 127.0.0.1:5434:5432 \
  postgres:16
```

> The Docker environment variable is stored in container metadata. This example is for a local disposable test database only, not production. Avoid sharing Docker inspection output. Use team-approved secret handling if available.

Wait until healthy/ready, using `docker ps` and `docker exec smart-event-postgres-test pg_isready -U smart_event_test -d smart_event_management_test`.

Build the URL safely (URL-encode special characters):

```bash
export TEST_DB_USER=smart_event_test
export TEST_DATABASE_URL="$(python3 - <<'PY'
import os
from urllib.parse import quote
user = quote(os.environ['TEST_DB_USER'], safe='')
password = quote(os.environ['TEST_DB_PASSWORD'], safe='')
print(f'postgresql+psycopg://{user}:{password}@127.0.0.1:5434/smart_event_management_test')
PY
)"
```

Check that it exists **without displaying the URL**:

```bash
test -n "$TEST_DATABASE_URL" && echo 'Isolated test DB URL configured'
```

Before running any database-changing operation, confirm the target is **your local test container**. Read `docs/backend/phase2-wsl-validation.md` for the project's test database safety requirements. Never bypass the integration-test safety guard.

### Alembic checks

```bash
cd ~/projects/Smart_Event_Management/backend
uv run python -m alembic history
uv run python -m alembic heads
DATABASE_URL="$TEST_DATABASE_URL" uv run python -m alembic current
```

The verified Phase 2 revision is `0001_initial_schema (head)`. On a **new, empty** isolated database, `current` may show no revision. **Do not run migrations on any shared or Supabase database.** For your newly created isolated local database only, after confirming the target and receiving team approval, run:

```bash
DATABASE_URL="$TEST_DATABASE_URL" uv run python -m alembic upgrade head
DATABASE_URL="$TEST_DATABASE_URL" uv run python -m alembic current
```

### Full backend verification

```bash
uv run python -m pytest -v
```

**Required acceptance:** `18 passed, 0 skipped` against the isolated local PostgreSQL test database, including:

- `test_concurrent_last_seat_registration`
- `test_concurrent_overlapping_venue_booking`

If 12 tests skip, `TEST_DATABASE_URL` is missing or rejected; do not claim full verification. Two known dependency deprecation warnings were non-blocking in the owner's verified environment.

## 6. Configure and verify the frontend

In Ubuntu:

```bash
cd ~/projects/Smart_Event_Management/frontend
npm ci
npm run typecheck
npm run build
```

Use `npm ci` if the repository includes a committed `package-lock.json`. Otherwise follow the package manager and lockfile committed to the repo; do not generate a competing lockfile.

For local development, inspect `frontend/package.json` for the available scripts, then run the documented dev command (commonly `npm run dev`). Open the localhost URL printed by the terminal.

The verified Phase 0 frontend was a **Next.js foundation**, not the completed Phase 7 product dashboard. Do not treat missing future dashboard features as setup failures. Frontend environment variables, if needed, must come from committed examples and the team-approved configuration.

## 7. Understand the existing architecture before coding

Current backend request path:

`Client → FastAPI router → authentication/dependencies → service → SQLAlchemy session → PostgreSQL → response`

Key locations:

| Area | Path |
|---|---|
| App entry and router registration | `backend/app/main.py` |
| API routes | `backend/app/api/` |
| Auth/security dependencies | `backend/app/core/` |
| Business rules and transactions | `backend/app/services/` |
| ORM models | `backend/app/models/` |
| Database/session | `backend/app/db/` |
| Request/response schemas | `backend/app/schemas/` |
| Alembic migrations | `backend/alembic/` (verify exact layout) |
| Backend tests | `backend/tests/` |
| Frontend | `frontend/` |
| Architecture and audit records | `docs/` |

Core implemented workflows: registration/login, JWT and Argon2, ADMIN/USER access control, profiles, venues and availability, events and cancellation, event registrations and cancellation, capacity rules, and concurrency protections.

**Important for Phase 3:** Agent tools should invoke existing services with typed inputs and appropriate authorization/confirmation rules. Do not bypass business logic by directly modifying database tables. Respect the approved existing API baseline; proposed roadmap-compatible changes require design review.

## 8. Git workflow for every teammate

1. Sync the agreed integration branch:

   ```bash
   git fetch origin
   git switch main
   git pull --ff-only origin main
   ```

2. Create a feature branch (example; follow your team's convention):

   ```bash
   git switch -c feat/phase3-agent-foundation
   ```

3. Make only assigned changes. Keep Phase 0–2 APIs and migrations stable unless the owner approves a change.
4. Before proposing a merge:

   ```bash
   git status
   git diff --check
   git diff --stat
   ```

5. Run relevant tests and frontend checks. Stage files intentionally (`git add <paths>` is safer than indiscriminate staging), inspect `git diff --cached`, commit, push the feature branch, and open a pull request.
6. Do not push directly to `main` unless the project owner explicitly requests it. Never commit `.env`, credentials, DB dumps, `.venv`, `node_modules`, `.next`, or generated caches.

## 9. Phase 3 handover: what is and is not ready

**Ready:** verified backend API, authentication/RBAC, SQLAlchemy services, isolated PostgreSQL tests, migrations, and architectural documentation.

**Not yet implemented as completed phases:** LLM/LangGraph orchestration, agent tools, RAG/vector search, complete dashboard/observability, and final deployment.

Before provider-specific Phase 3 implementation, the owner must resolve the deferred LLM/embedding provider decision (ADR-009). Hosting-specific decisions (ADR-010) can remain deferred until deployment-specific work. Never put API keys in source code.

## 10. Troubleshooting quick reference

| Symptom | Check / action |
|---|---|
| `wsl` access error | Restart Windows; check `wsl --status`; do not unregister Ubuntu |
| `uv: command not found` | Install `uv` in Ubuntu and restart shell |
| `node` missing or Windows npm used in WSL | Install Linux-native Node.js and confirm `which node` |
| `docker: command not found` | Start Docker Desktop, enable Ubuntu WSL integration, reopen terminal |
| Port 5434 already used | Check `docker ps` and local listeners; coordinate before changing port |
| 12 integration tests skipped | Confirm `TEST_DATABASE_URL` exists and points to approved isolated DB |
| Alembic `current` empty | New isolated DB may not yet be migrated; verify target before approved migration |
| `/api/ready` not HTTP 200 | Inspect local application DB availability/configuration; never use production to bypass failure |
| Git says secret or generated file staged | Unstage it, check `.gitignore`, and rotate any leaked credential |
| TypeScript/Next build errors | Check Node version, lockfile, Linux-native tooling, and documented scripts |

## 11. Mandatory onboarding checklist

Each teammate must report these results to the project owner before starting assigned development:

- [ ] Repository access granted; clone completed successfully.
- [ ] VS Code opens the correct Ubuntu/WSL workspace.
- [ ] Git, Python, `uv`, Linux-native Node/npm and Docker verified.
- [ ] Phase 0–2 completion reports, architecture decisions and API baseline read.
- [ ] Local secrets configured without committing or sharing them.
- [ ] Local isolated PostgreSQL 16 database created or verified.
- [ ] Alembic revision confirmed as `0001_initial_schema (head)` on the **isolated** database.
- [ ] Full backend suite reports **18 passed, 0 skipped**.
- [ ] Both concurrency tests passed.
- [ ] FastAPI starts; `/api/health`, `/api/ready`, `/openapi.json` return HTTP 200.
- [ ] Frontend typecheck and build pass using the committed package manager.
- [ ] Feature branch created; assigned work and integration expectations confirmed.
- [ ] No Supabase/production tests, unapproved migrations, or secrets in Git.

### Teammate onboarding report template

```text
Name / assigned phase-task:
Operating system and Ubuntu version:
Git / Python / uv / Node / npm versions:
Docker/PostgreSQL local status:
Repository commit SHA (git rev-parse --short HEAD):
Backend tests: __ passed, __ skipped, __ failed
Concurrency tests: __ / 2 passed
Isolated DB Alembic current:
FastAPI startup: PASS / FAIL
Health / Ready / OpenAPI HTTP status:
Frontend typecheck: PASS / FAIL
Frontend build: PASS / FAIL
Feature branch:
Blockers (no credentials or full DB URLs):
```

**Onboarding approval:** The project owner reviews the report and confirms readiness before assigning implementation work.
