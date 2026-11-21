# System architecture

```mermaid
flowchart LR
 U[Browser] --> F[Next.js frontend]
 F --> API[FastAPI API]
 API --> AUTH[Auth/RBAC]
 API --> SVC[Business services]
 SVC --> DB[(PostgreSQL + pgvector)]
 API --> G[LangGraph]
 G --> T[Controlled tools]
 T --> SVC
 G --> R[RAG retrieval]
 R --> DB
 API --> O[Audit/observability]
```

The system is a monorepo with a browser, API boundary, business services, persistence, agent orchestration and retrieval. The enforced path is **LLM → LangGraph → controlled tools → business services → database**. The LLM never connects to PostgreSQL.

## Authentication flow

```mermaid
sequenceDiagram
 participant C as Client
 participant A as Auth API
 participant U as Users
 C->>A: register/login credentials
 A->>U: hash or verify password
 U-->>A: user + role
 A-->>C: short-lived JWT
 C->>A: Bearer JWT request
 A->>A: verify signature, expiry, role and object access
```

## Event registration workflow

```mermaid
sequenceDiagram
 participant P as Participant
 participant API as API
 participant S as RegistrationService
 participant DB as PostgreSQL
 P->>API: register(event)
 API->>S: authenticated user + event
 S->>DB: transaction/lock event
 S->>DB: check status, duplicate and capacity
 DB-->>S: permitted
 S->>DB: insert registration
 S-->>API: registration
 API-->>P: 201 result
```

## Event cancellation workflow

```mermaid
sequenceDiagram
 participant A as Admin
 participant API as API
 participant S as EventService
 participant DB as PostgreSQL
 A->>API: cancel(event, confirmation)
 API->>S: verify ADMIN and confirmation
 S->>DB: transaction: mark cancelled
 S->>DB: audit and notify affected registrations
 DB-->>S: committed
 S-->>API: cancelled event
 API-->>A: result
```

