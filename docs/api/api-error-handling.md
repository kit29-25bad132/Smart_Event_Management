# API error handling

Use 400 malformed request, 401 missing/invalid token, 403 insufficient role/object access, 404 missing resource, 409 business conflict, 422 schema validation, 429 rate limit, and 500/503 controlled server/dependency failures. Never expose stack traces, SQL, secrets, password hashes or provider prompts. Include request ID and stable machine-readable code.

