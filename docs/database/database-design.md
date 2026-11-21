# Database design

PostgreSQL is the system of record. UUID primary keys are recommended. Timestamps are UTC `timestamptz`. Domain state changes are soft/auditable; registration cancellation and event cancellation do not delete history. pgvector stores embeddings on `knowledge_chunks.embedding`.

Entities: `users` owns identity/role; `venues` is a bookable location; `events` belongs to a creator and venue; `registrations` joins users and events; `agent_sessions` and `agent_runs` group assistant activity; `tool_calls` records controlled actions; `knowledge_documents` versions source files; `knowledge_chunks` stores searchable pieces; `audit_logs` records security-relevant actions.

Registration uses a transaction that locks the event row (or uses a serializable/atomic capacity constraint), checks active count and unique `(event_id,user_id)`, then inserts. Venue booking checks overlapping active event ranges under a transaction and an exclusion/range constraint where supported.

