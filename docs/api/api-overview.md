# API overview

Base path `/api`; JSON over HTTPS; JWT `Authorization: Bearer <token>`. Common success codes are 200/201/204. Errors use `{ "error": { "code": "...", "message": "...", "request_id": "...", "details": {} } }`. Pagination uses `page`, `page_size`, and stable ordering. Recommended (REC) endpoints are labeled separately from mandatory endpoints.

