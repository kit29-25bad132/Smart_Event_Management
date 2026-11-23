# Phase 3 to Final Implementation Plan

The checked-in eight-week roadmap maps later work as follows. Planned work is not represented as completed functionality.

## Phase 3 — Agent foundation / roadmap Week 5

Objective: introduce a controlled agent boundary over existing deterministic services.

Prerequisites: verified Phase 2 API/services, approved LLM provider, secret storage, tool contracts.

Tasks: add typed agent state, intent classification, LangGraph nodes/edges, authentication context propagation, event search/create/detail tools, confirmation for writes, audit events and unit tests. Suggested locations: `backend/app/agent/`, `backend/app/tools/`, new provider/config modules.

Acceptance: an authenticated request routes only to an authorized tool; tool validation and service rules remain authoritative; read and write workflows have deterministic tests; no direct database access from the LLM.

## Phase 4 — Event operations / roadmap Week 5–6

Add registration/cancellation, venue availability, event update/cancel tools and multi-step workflows. Reuse `event_service`, `registration_service`, venue services and existing RBAC. Test confirmation, refusal, rollback, capacity and concurrency behavior through tool boundaries.

## Phase 5 — Knowledge RAG / roadmap Week 6

Add policy/FAQ source versioning, ingestion/chunking, embeddings, pgvector schema and semantic retrieval with citations. Define document authorization and prompt-injection handling. Acceptance requires grounded answers, source citations, insufficient-evidence responses and retrieval tests.

## Phase 6 — Agent plus RAG / roadmap Week 6

Route business requests to business tools and policy questions to retrieval; support combined workflows with explicit boundaries. Add routing, evaluation, hallucination and authorization tests.

## Phase 7 — Frontend and observability / roadmap Week 7

Implement authentication, dashboard, event/venue/registration screens, AI chat and role-aware navigation. Add structured request/agent/tool metrics, latency/error tracking and privacy-safe logs. Acceptance includes typecheck/build, API integration, accessibility and role tests.

## Phase 8 — Testing and delivery / roadmap Week 8

Add CI, Docker packaging, deployment configuration, migration gates, security review, load/reliability checks, monitoring and rollback documentation. Acceptance requires reproducible CI, isolated test DB, deploy smoke tests, secret scanning and operational runbooks.

## Cross-cutting risks

Provider cost/availability, prompt injection, tool authorization drift, vector-data privacy, migration compatibility, frontend/backend contract drift and observability of asynchronous workflows. Every phase needs a short design review and an integration checkpoint before merging.
