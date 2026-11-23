# Completed Work Inventory

## Foundation

- Monorepo with `backend/` and `frontend/`.
- Next.js 15/React 19/TypeScript/Tailwind landing and status page.
- FastAPI app with `/api/health`, `/api/ready`, OpenAPI and Swagger routes.
- Python `uv` manifest/lockfile, frontend npm lockfile, environment examples and ignore rules.
- Setup, architecture, requirements and roadmap documentation.

## Phase 1 design

- Functional/non-functional requirements, MVP scope, user stories, use cases and acceptance criteria.
- Backend, system, frontend, deployment, observability, agent and RAG architecture documents.
- Database ER/data dictionary/constraints/decisions documentation.
- API reference and error contract documentation.

## Phase 2 backend

- Configuration through Pydantic Settings (`backend/app/core/config.py`).
- JWT security and Argon2 password hashing (`backend/app/core/security.py`).
- Current-user and admin dependencies (`backend/app/core/dependencies.py`).
- Auth, user, venue, event and registration routers under `backend/app/api/`.
- Service-layer business rules under `backend/app/services/`.
- SQLAlchemy models for users, venues, events and registrations.
- Alembic initial schema revision with PostgreSQL enums, keys, indexes and constraints.
- Standardized HTTP, validation, integrity and internal-error envelopes in `backend/app/main.py`.
- Row locks for registration capacity and venue conflict races.
- Unit, error-contract, configuration and safety-gated PostgreSQL integration tests.
- Reported WSL results: 18 tests and both concurrency tests passed; these are historical until reproduced by the receiving team.

## Intentionally not implemented

- LangGraph runtime, LLM provider integration and agent tools.
- Policy/FAQ ingestion, embeddings, pgvector retrieval and citations.
- Product dashboard, event/registration/venue pages and AI chat UI.
- Agent activity telemetry, production CI/CD, container deployment and monitoring.
- Notifications and other roadmap-later integrations.
