# Constraints and indexes

Unique normalized user email; positive venue/event capacity; `ends_at > starts_at`; valid status transitions; foreign keys with restrictive delete for history. Index users email, events `(status, starts_at)`, events venue/time, registrations `(event_id,status)`, registrations user/status, agent runs session/time, tool calls run/time, documents hash/status, and audit actor/time. Use HNSW or IVFFlat on pgvector after measuring embedding dimension and workload. Add exclusion/range protection for overlapping active venue bookings where business semantics permit.

