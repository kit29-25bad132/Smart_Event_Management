# Agentic AI Smart Event Management System

Phase 0 establishes the development foundation for an internship project that will grow into an event-management platform with agentic AI workflows.

## Implemented now

- Next.js, React, TypeScript, and Tailwind landing page
- FastAPI application with `/api/health` and `/api/ready`
- Environment-based frontend API URL and backend CORS
- Basic backend tests and Windows PowerShell setup documentation
- Phase 2 non-AI backend foundation: PostgreSQL/SQLAlchemy/Alembic design, JWT authentication, RBAC, venues, events and registrations

Domain features, authentication, database, AI agents, RAG, dashboards, and deployment are planned only.

Phase 2 now implements the non-AI domain backend. AI agents, RAG, embeddings, notifications, and frontend product screens remain planned.

## Stack

Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS. Backend: Python 3.12–3.14, FastAPI, Pydantic Settings, Uvicorn. Future: PostgreSQL, SQLAlchemy, Alembic, LangGraph, pgvector, Pytest, Docker.

## Setup

Windows PowerShell, Git, Node.js 24+, npm 11+, Python 3.12–3.14, and optionally Docker. Follow [docs/setup-guide.md](docs/setup-guide.md). Real `.env` files are ignored.

## Validation

Backend (Windows): `cd backend; .venv\Scripts\Activate.ps1; python -m pytest -v`. Backend (WSL2): `cd /mnt/c/Users/kit29/Desktop/Smart_Event_Management/backend; uv sync --locked --extra dev; uv run python -m pytest -v`. Frontend: `cd frontend; npm run typecheck; npm run build`. A successful readiness check additionally requires a configured, reachable development PostgreSQL database. Run both applications to verify the browser status card reports `connected`.

See [docs/architecture.md](docs/architecture.md) and [docs/development-roadmap.md](docs/development-roadmap.md).

Backend implementation details are in [docs/backend/backend-setup.md](docs/backend/backend-setup.md).
