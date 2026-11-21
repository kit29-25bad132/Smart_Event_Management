# Events API

`POST /api/events` ADMIN: event JSON `{title,description,venue_id,starts_at,ends_at,capacity,status}` → 201. `GET /api/events` public/authenticated: filters `q,status,venue_id,starts_from,starts_to,page,page_size` → paginated 200. `GET /api/events/{id}` public → 200. `PATCH /api/events/{id}` ADMIN → 200. `POST /api/events/{id}/cancel` ADMIN → 200. Errors: 401/403/404/409 venue conflict/422 invalid dates or capacity. Cancelled events reject new registrations.

