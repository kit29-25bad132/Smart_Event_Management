# API reference

The interactive OpenAPI document is available at `/docs` when the backend runs, and the schema at `/openapi.json`. Implemented groups: `/api/auth`, `/api/users`, `/api/venues`, `/api/events`, and `/api/events/{id}/register` plus `/api/registrations/me`. Public event discovery returns published events only; drafts are administrator-managed. Errors use the documented `error.code`, `error.message`, `error.request_id`, and `error.details` envelope. AI/RAG endpoints remain planned and are not registered in Phase 2.

