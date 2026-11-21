# Functional requirements

The items below are the mandatory product requirements derived from the supplied Infosys roadmap. Engineering recommendations are marked **REC**.

| ID | Requirement | Actor | Preconditions | Expected behaviour | Priority | Dependencies |
|---|---|---|---|---|---|---|
| FR-AUTH-001 | Register an account with unique email and password | USER | None | Validate input, hash password, create USER account | Must | DB users |
| FR-AUTH-002 | Log in and receive JWT access token | USER | Registered account | Verify credentials and issue short-lived token | Must | FR-AUTH-001 |
| FR-AUTH-003 | Enforce ADMIN/USER role-based access | System | Authenticated request | Authorize endpoint and tool by role | Must | FR-AUTH-002 |
| FR-EVENT-001 | Create an event with date/time, venue, capacity and status | ADMIN | Authenticated ADMIN; venue exists | Validate capacity and availability, persist draft/published event | Must | FR-VENUE-001 |
| FR-EVENT-002 | View, search and filter events | USER/ADMIN | None | Return paginated events matching filters | Must | FR-EVENT-001 |
| FR-EVENT-003 | Update an event | ADMIN | Event exists and is editable | Apply validated changes and re-check venue conflicts | Must | FR-EVENT-001 |
| FR-EVENT-004 | Cancel an event | ADMIN | Event exists | Mark cancelled, prevent new registrations, preserve history | Must | FR-EVENT-001 |
| FR-VENUE-001 | Create and manage venues with capacity/location | ADMIN | Authenticated ADMIN | Persist venue and validate positive capacity | Must | users |
| FR-VENUE-002 | Check venue availability for a time range | ADMIN | Venue exists; valid range | Return conflict/available result | Must | FR-EVENT-001 |
| FR-REG-001 | Register a participant for an event | USER/ADMIN | Authenticated; event open | Atomically validate capacity and duplicate state, then create registration | Must | FR-EVENT-002 |
| FR-REG-002 | Cancel a registration | USER/ADMIN | Registration exists; actor owns it or is ADMIN | Mark cancelled and release seat | Must | FR-REG-001 |
| FR-REG-003 | View registrations and status | USER/ADMIN | Authenticated | Scope USER results to self; ADMIN may inspect managed events | Must | FR-REG-001 |
| FR-AI-001 | Understand natural-language event requests | USER/ADMIN | Authenticated AI session | Classify intent and extract validated parameters | Must | FR-AUTH-003 |
| FR-AI-002 | Select controlled tools and execute multi-step workflows | USER/ADMIN | Authorized intent | LangGraph routes only to authorized business tools | Must | FR-AI-001 |
| FR-AI-003 | Return final response with workflow outcome | USER/ADMIN | Workflow completed or failed | Explain result, uncertainty and next action | Must | FR-AI-002 |
| FR-RAG-001 | Ingest, chunk, embed and store policy/FAQ documents | ADMIN/System | Approved document | Version document and searchable chunks in pgvector | Must | knowledge tables |
| FR-RAG-002 | Answer policy/FAQ questions with grounded sources | USER/ADMIN | Indexed documents | Retrieve semantic context, answer only from evidence, cite sources | Must | FR-RAG-001 |
| FR-DASH-001 | Provide dashboard, event, registration, venue and AI activity views | USER/ADMIN | Authenticated | Show role-scoped statistics and activity | Must | all domain APIs |
| FR-OBS-001 | Record audit, agent run and tool-call activity | System | Relevant operation | Persist structured event without secrets | Must | audit tables |

Validation and failure rules: email is normalized and unique; passwords are never stored or logged; event end must follow start; capacity is positive; registration is rejected for cancelled/closed/full events, duplicate active registration, or invalid identity; destructive AI requests require explicit confirmation; unknown policy answers must state that evidence is unavailable. Recommended additions: FR-REC-001 pagination defaults, FR-REC-002 idempotency keys, FR-REC-003 rate limits.
