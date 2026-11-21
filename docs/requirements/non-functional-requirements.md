# Non-functional requirements

| ID | Requirement | Measure / acceptance |
|---|---|---|
| NFR-SEC-001 | Passwords use Argon2id or bcrypt; JWT secrets come from secret storage | No plaintext credentials in code, logs or responses |
| NFR-SEC-002 | RBAC and object-level authorization | Unauthorized role/object requests return 401/403 |
| NFR-SEC-003 | Validate all JSON, query and tool inputs | Invalid input returns structured 422 |
| NFR-SEC-004 | Resist prompt/document injection | Retrieved text is untrusted data; tools remain allow-listed |
| NFR-PERF-001 | Paginated list endpoints | p95 target <500 ms excluding external LLM calls |
| NFR-PERF-002 | Registration transaction safety | No oversell or duplicate active registration under concurrency |
| NFR-REL-001 | Health/readiness and graceful failures | Dependency failure is observable and returns stable error shape |
| NFR-OBS-001 | Correlate request, agent run and tool call IDs | Logs contain IDs but no secrets or raw sensitive prompts |
| NFR-DATA-001 | Retain audit history and soft-delete where required | Cancellations preserve records and actor/time |
| NFR-MAINT-001 | Typed contracts, migrations and automated tests | CI blocks invalid type checks, tests and migrations |
| NFR-DEP-001 | Reproducible local and hosted deployment | Versioned configuration; no credentials in repository |

