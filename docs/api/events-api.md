# Events API

Target contract: `POST /api/events` ADMIN creates event JSON `{title,description,venue_id,starts_at,ends_at,capacity,status}` → 201. `GET /api/events` supports public discovery, `q`, `status`, `venue_id`, `page`, and `page_size`; the current Phase 2 implementation returns an array rather than a `{items,total}` envelope and does not yet expose `starts_from`/`starts_to`. `GET /api/events/{id}` public → 200 for published events. `PATCH /api/events/{id}` ADMIN → 200. `POST /api/events/{id}/cancel` ADMIN → 200. Errors: 401/403/404/409 venue conflict/422 invalid dates or capacity. Cancelled events reject new registrations. The target pagination/date-filter contract remains a documented follow-up, not an undocumented implementation claim.

