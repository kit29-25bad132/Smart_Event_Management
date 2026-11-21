# Registrations API

`POST /api/events/{event_id}/registrations` USER/ADMIN: `{participant_user_id?}`; USER may only register self, ADMIN may act for a participant → 201. `GET /api/registrations/me` returns own registrations. `GET /api/events/{event_id}/registrations` ADMIN returns event registrations. `POST /api/registrations/{id}/cancel` owner/ADMIN → 200. Transaction enforces capacity, duplicate prevention and event status. Errors: 401/403/404/409 full/duplicate/closed/422.

