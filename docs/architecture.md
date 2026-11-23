# Architecture

The repository contains a Next.js/TypeScript frontend and a FastAPI/Pydantic backend. The browser calls the backend through `NEXT_PUBLIC_API_URL`; CORS is configured with `BACKEND_CORS_ORIGINS`.

Phase 2 implements the non-AI layers: API routes, authentication/RBAC, services, SQLAlchemy models, Alembic migrations, PostgreSQL persistence, venues, events and registrations. LangGraph orchestration, business-agent tools, RAG/pgvector runtime, product dashboard, and production observability remain planned for later phases. The detailed designs in `docs/architecture/` describe those future interfaces and must not be read as implemented runtime components.
