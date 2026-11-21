# Deployment architecture

Proposed deployment: Next.js hosted frontend → HTTPS FastAPI service → private managed PostgreSQL with pgvector. Secrets come from the hosting secret manager. CI runs lint/type/test/build/migration checks. Docker is a packaging option; Phase 0 does not activate database or production services.

