# Database decisions

Accepted: PostgreSQL is authoritative; UUIDs and UTC timestamps; soft/auditable cancellation. Proposed: SQLAlchemy + Alembic, pgvector, row locking/serializable registration transaction, and exclusion constraint for venue time ranges. Pending: exact enum values, retention periods, embedding model/dimension, and provider-specific vector index parameters.

