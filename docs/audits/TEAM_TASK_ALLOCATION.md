# Team Task Allocation

Use workstream ownership rather than assuming a fixed team size. Each workstream owns code, tests and documentation, while interfaces are reviewed jointly.

| Workstream | Owns | Depends on | Integration checkpoint |
|---|---|---|---|
| Agent orchestration | LangGraph state, routing, retries, confirmations | Phase 2 auth/service contracts | Typed tool contract review |
| Business tools | Event, venue, registration tool adapters | Existing services and RBAC | Tool authorization/concurrency tests |
| RAG | Ingestion, chunking, embeddings, retrieval and citations | Approved document/vector decisions | Retrieval evaluation |
| Frontend | Auth, dashboard, event/registration pages, chat | Stable API/OpenAPI and agent endpoint | End-to-end role workflow |
| Observability | Request, agent, tool metrics and safe logs | Agent and API events | Privacy/security review |
| QA/reliability | Contract, integration, concurrency, evaluation and regression suites | All workstreams | Release candidate gate |
| Delivery/security | CI, Docker, secrets, migrations, deployment and monitoring | Stable backend/frontend artifacts | Staging smoke and rollback drill |

## Parallelization

Agent orchestration, RAG design/fixture preparation, frontend wireframes and CI scaffolding can proceed in parallel after the Phase 2 contract freeze. Tool adapters must wait for the agent state/tool interface. Frontend integration must wait for stable endpoint schemas. Deployment must wait for reproducible tests and migration approval.

## Collaboration rules

- Use short-lived branches and pull requests; do not commit secrets or `.env` files.
- Every PR includes tests, documentation updates and a statement of database impact.
- Database changes include an Alembic migration, rollback analysis and isolated validation evidence.
- Reviewers verify authorization at both route and service/tool boundaries.
- No agent feature may bypass deterministic business services.
- Integration checkpoints require green backend tests, frontend typecheck/build where applicable, and sanitized logs.
