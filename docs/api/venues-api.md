# Venues API

`POST /api/venues` ADMIN creates `{name,capacity,location}` → 201. `GET /api/venues` authenticated lists active venues. `GET /api/venues/{id}` returns details. `PATCH /api/venues/{id}` ADMIN updates metadata/capacity subject to existing-event rules. `GET /api/venues/{id}/availability?starts_at=&ends_at=` authenticated → `{available,conflicts}`. Errors include 409 overlap and 422 invalid range.

