# ER diagram

```mermaid
erDiagram
 USERS ||--o{ EVENTS : creates
 USERS ||--o{ REGISTRATIONS : makes
 VENUES ||--o{ EVENTS : hosts
 EVENTS ||--o{ REGISTRATIONS : receives
 USERS ||--o{ AGENT_SESSIONS : owns
 AGENT_SESSIONS ||--o{ AGENT_RUNS : contains
 AGENT_RUNS ||--o{ TOOL_CALLS : invokes
 KNOWLEDGE_DOCUMENTS ||--o{ KNOWLEDGE_CHUNKS : contains
 USERS ||--o{ AUDIT_LOGS : causes
 USERS { uuid id PK; string email UK; string role }
 VENUES { uuid id PK; string name; int capacity }
 EVENTS { uuid id PK; uuid venue_id FK; uuid created_by FK; timestamptz starts_at; timestamptz ends_at }
 REGISTRATIONS { uuid id PK; uuid event_id FK; uuid user_id FK; string status }
 AGENT_SESSIONS { uuid id PK; uuid user_id FK }
 AGENT_RUNS { uuid id PK; uuid session_id FK }
 TOOL_CALLS { uuid id PK; uuid run_id FK }
 KNOWLEDGE_DOCUMENTS { uuid id PK; string version }
 KNOWLEDGE_CHUNKS { uuid id PK; uuid document_id FK; vector embedding }
 AUDIT_LOGS { uuid id PK; uuid actor_id FK }
```

