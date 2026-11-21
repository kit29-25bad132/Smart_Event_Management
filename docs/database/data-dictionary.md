# Data dictionary

| Entity | Columns (type; key/default; nullable; purpose) |
|---|---|
| users | `id uuid PK`; `email citext UNIQUE NOT NULL`; `password_hash text NOT NULL`; `role enum NOT NULL DEFAULT USER`; `is_active boolean DEFAULT true`; `created_at/updated_at timestamptz NOT NULL` |
| venues | `id uuid PK`; `name text NOT NULL`; `capacity integer CHECK >0`; `location text NOT NULL`; `is_active boolean DEFAULT true`; timestamps |
| events | `id uuid PK`; `created_by uuid FK users`; `venue_id uuid FK venues`; `title/description text`; `starts_at/ends_at timestamptz NOT NULL`; `capacity integer CHECK >0`; `status enum`; timestamps |
| registrations | `id uuid PK`; `event_id/user_id uuid FK`; `status enum DEFAULT ACTIVE`; `registered_at/cancelled_at timestamptz`; UNIQUE active participant/event |
| agent_sessions | `id uuid PK`; `user_id FK`; `status`; timestamps |
| agent_runs | `id uuid PK`; `session_id FK`; `intent`; `status`; `error_code`; started/completed timestamps |
| tool_calls | `id uuid PK`; `run_id FK`; `tool_name`; redacted input/output JSONB; `status`; duration; timestamps |
| knowledge_documents | `id uuid PK`; `source_uri`; `title`; `mime_type`; `content_hash`; `version`; `status`; timestamps |
| knowledge_chunks | `id uuid PK`; `document_id FK`; `chunk_index`; `content`; `token_count`; `embedding vector`; metadata JSONB |
| audit_logs | `id uuid PK`; `actor_id FK nullable`; action/resource identifiers; outcome; metadata JSONB; `created_at` |

