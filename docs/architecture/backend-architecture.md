# Backend architecture

FastAPI routes own HTTP contracts and dependency injection. Core owns settings, JWT and logging. Services own business rules and transactions. Repositories/SQLAlchemy own persistence. Schemas are Pydantic request/response types. Agent and RAG adapters call services and retrieval interfaces, never tables directly.

```mermaid
flowchart TB
 R[Routes] --> D[Auth dependencies]
 R --> S[Business services]
 S --> Repo[Repositories/ORM]
 Repo --> PG[(PostgreSQL)]
 Agent[Agent adapter] --> S
 RAG[RAG adapter] --> Repo
```

