# API Contract Decision Record

## Status

**Approved baseline — project owner approval recorded in the Phase 1 closure request.** The official roadmap was read from `C:\Users\kit29\Downloads\Infosys_Agentic_AI_Smart_Event_Management_Complete_Roadmap (1).pdf`, titled “Agentic AI Smart Event Management System Complete Project Roadmap, Requirements, Architecture, Tools & Technology 8-Week Implementation & Training Plan.” The PDF has 14 pages; no version/date was visible in the extracted document text. It is not currently stored in the repository.

## Endpoint comparison

| Capability | Target/documented contract | Current Phase 2 implementation | Difference |
|---|---|---|---|
| Event search | Roadmap §9: `GET /api/events`; repository target adds filters/pagination | `GET /api/events` with `q`, `status`, `venue_id`, `page`, `page_size`; returns an array | Date filters and response envelope are future evolution items |
| Event update/cancel | Roadmap §9: `PUT /api/events/{id}`, `DELETE /api/events/{id}` | Current Phase 2 uses `PATCH /api/events/{id}` and cancellation routes `DELETE /api/events/{id}` plus `POST /api/events/{id}/cancel` | Preserve tested current routes; document PUT/DELETE as target compatibility/evolution reference |
| Registration | Roadmap §9: `POST /api/events/{id}/register` | Implemented exactly | No difference |
| Registration cancellation/listing | Roadmap §9: `DELETE /api/events/{id}/register`, `GET /api/events/{id}/registrations`, `GET /api/registrations/me` | Implemented exactly | No difference |
| User administration | Roadmap §3–4 requires identity/roles; it does not prescribe user-admin paths | Current Phase 2 exposes profile and admin user listing | Additional role-management routes remain later scope, not a Phase 1 design failure |

## Recommendation

The project owner approves the current Phase 2 routes as the stable implementation baseline. Before agent tools are implemented:

1. retain current tested routes and add compatibility aliases only when needed; or
2. deliberately evolve the contract with versioned/client-reviewed changes.

Do not silently change routes or add agent wrappers around an unresolved contract.

## ADR-009 and ADR-010 decisions

- **ADR-009 LLM/embedding provider:** no approved provider decision exists. Decision owner: project/internship technical lead with data-residency/security owner. Prerequisites: approved roadmap, data classification, budget, latency, provider retention and embedding-dimension review. Deadline: before Phase 3 provider integration and before RAG schema/index implementation. Phase 1 acceptance may defer provider selection because the design explicitly marks it Pending, but must record owner approval of that deferral.
- **ADR-010 deployment hosting:** no approved hosting decision exists. Decision owner: project/internship technical lead with DevOps/reviewer. Prerequisites: deployment constraints, budget, network/security requirements, PostgreSQL/pgvector availability and CI expectations. Deadline: before Phase 8 deployment implementation. Phase 1 acceptance may defer hosting selection because deployment is a later roadmap phase, subject to owner approval of the deferral.

## Approval record

Current status for this repository: **APPROVED BASELINE**. Approval is the project owner authorization supplied with the Phase 1 closure request. The implementation baseline remains current Phase 2 behavior; roadmap target variants remain documented rather than silently substituted.
