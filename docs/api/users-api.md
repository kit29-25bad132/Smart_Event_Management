# Users API

`GET /api/users/me` (authenticated USER/ADMIN) returns own profile. `PATCH /api/users/me` updates allowed profile fields. `GET /api/users/{user_id}` is ADMIN-only and returns a redacted profile. `PATCH /api/users/{user_id}/role` is ADMIN-only and changes role with audit record. Path identity is never taken from natural-language input.

