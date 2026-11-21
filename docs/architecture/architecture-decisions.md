# Architecture decisions

| ADR | Decision | Status | Rationale / alternatives |
|---|---|---|---|
| ADR-001 | Monorepo with `frontend`, `backend`, `docs` | Accepted | Simple internship delivery; polyrepo deferred |
| ADR-002 | Next.js App Router | Accepted | Required stack and typed React UI |
| ADR-003 | FastAPI + Pydantic | Accepted | Required stack; clear API contracts |
| ADR-004 | PostgreSQL | Accepted | Transactional relational domain |
| ADR-005 | SQLAlchemy ORM + Alembic | Proposed | Maintainable mappings and migrations; raw SQL alternative |
| ADR-006 | LangGraph | Proposed | Explicit stateful workflows and conditional edges |
| ADR-007 | pgvector | Proposed | Co-located semantic retrieval; external vector DB alternative |
| ADR-008 | JWT access tokens | Proposed | Stateless API authorization; secure cookie/session alternative |
| ADR-009 | LLM/embedding provider | Pending | Depends on cost, data residency and internship approval; no provider assumed |
| ADR-010 | Deployment hosting | Pending | Compare managed frontend/API/Postgres options after constraints are known |

