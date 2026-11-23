# Gaps and Remediation Plan

| ID | Severity | Gap | Evidence | Recommended remediation | Effort | Blocks Phase 3? |
|---|---|---|---|---|---|---|
| AUD-001 | BLOCKER | Official Infosys roadmap PDF/source is absent | Repository search; only `docs/development-roadmap.md` found | Add the approved roadmap to the project or record an explicit owner-approved substitute | Small | Conditional |
| AUD-002 | CRITICAL | PostgreSQL runtime/migration evidence is historical in this audit | `docs/backend/phase2-wsl-validation.md`; user-reported results | Re-run isolated integration suite, Alembic history/heads/current and endpoint smoke checks; archive outputs without secrets | Small | Yes for formal Phase 2 sign-off |
| AUD-003 | HIGH | Production role-management workflow is not demonstrated | `backend/app/core/dependencies.py`; routers; no admin role endpoint found | Confirm intentional scope; if required, design an audited admin-only role-management operation | Medium | No, unless roadmap requires it |
| AUD-004 | HIGH | Frontend is only a landing/status page | `frontend/src/app/page.tsx`; frontend architecture | Implement dashboard, auth, event, registration and chat workstreams in later phases | Large | No |
| AUD-005 | HIGH | Agent/RAG are design-only | `backend/app/agent/__init__.py`; `backend/app/rag/__init__.py`; architecture docs | Implement controlled tool interfaces and retrieval incrementally; do not let LLMs bypass services | Large | No, Phase 3 begins here |
| AUD-006 | MEDIUM | No CI workflow was found | Repository file inventory | Add CI for backend tests, frontend typecheck/build, migration offline checks and secret scanning | Medium | No |
| AUD-007 | MEDIUM | CORS is permissive for methods/headers | `backend/app/main.py:25` | Restrict methods/headers and production origins during deployment hardening | Small | No |
| AUD-008 | MEDIUM | Documentation has multiple environment assumptions | README, setup guide, WSL guide | Choose a canonical WSL/local DB workflow and keep Windows instructions as a supported alternative | Small | No |
| AUD-009 | LOW | Some code is densely semicolon-compressed | routers/services/tests | Apply formatting/linting in a separate approved maintenance change | Small | No |

## Highest-priority sequence

1. Confirm the official roadmap and stakeholder acceptance baseline.
2. Reproduce isolated PostgreSQL migration, full tests and smoke checks.
3. Record the verified Phase 2 baseline and freeze the service/API contracts.
4. Start agent tool interfaces against existing services.
5. Add CI and security checks before parallel team delivery expands.
