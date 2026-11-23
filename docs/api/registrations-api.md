# Registrations API

Target contract: participant registration is USER/ADMIN with optional `participant_user_id`, and cancellation is owner/ADMIN. Current Phase 2 paths are `POST /api/events/{event_id}/register`, `DELETE /api/events/{event_id}/register`, `GET /api/registrations/me`, and `GET /api/events/{event_id}/registrations`. The implemented register/cancel paths operate on the authenticated user; the target participant-acting and registration-ID cancellation variants are not yet implemented. Transaction logic enforces capacity, duplicate prevention and event status. Errors: 401/403/404/409 full/duplicate/closed/422. This route/behavior difference is recorded for explicit contract approval before future agent tools are built.

