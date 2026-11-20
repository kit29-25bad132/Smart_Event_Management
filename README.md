# Agentic AI Smart Event Management System

Phase 0 establishes the development foundation for an internship project that will grow into an event-management platform with agentic AI workflows.

## Implemented now

- Next.js, React, TypeScript, and Tailwind landing page
- FastAPI application with `/api/health` and `/api/ready`
- Environment-based frontend API URL and backend CORS
- Basic backend tests and Windows PowerShell setup documentation

Domain features, authentication, database, AI agents, RAG, dashboards, and deployment are planned only.

## Stack

Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS. Backend: Python 3.12–3.14, FastAPI, Pydantic Settings, Uvicorn. Future: PostgreSQL, SQLAlchemy, Alembic, LangGraph, pgvector, Pytest, Docker.

## Setup

Windows PowerShell, Git, Node.js 24+, npm 11+, Python 3.12–3.14, and optionally Docker. Follow [docs/setup-guide.md](docs/setup-guide.md). Real `.env` files are ignored.

## Validation

Backend: `cd backend; .venv\Scripts\Activate.ps1; pytest`. Frontend: `cd frontend; npm run typecheck; npm run build`. Run both applications to verify the browser status card reports `connected`.

See [docs/architecture.md](docs/architecture.md) and [docs/development-roadmap.md](docs/development-roadmap.md).
