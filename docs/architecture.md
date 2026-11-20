# Architecture

Phase 0 contains a Next.js/TypeScript frontend and a FastAPI/Pydantic backend. The browser calls the backend through `NEXT_PUBLIC_API_URL`; CORS is configured with `BACKEND_CORS_ORIGINS`.

Planned layers are API routes, services, database models/migrations, agent orchestration, business tools, RAG, and observability. PostgreSQL/pgvector, LangGraph, authentication, and domain features are intentionally not implemented yet.
