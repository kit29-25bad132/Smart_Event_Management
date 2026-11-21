# Authentication API

`POST /api/auth/register` (public): `{email,password}` → 201 `{user,access_token}`; validates email/password and assigns USER. `POST /api/auth/login` (public): credentials → 200 token; invalid credentials → 401. `POST /api/auth/refresh` (authenticated/REC): refresh token → 200 rotated access token. `GET /api/auth/me` (authenticated): → 200 current user. Errors: 409 duplicate, 422 validation, 429 rate limit.

