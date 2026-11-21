# Acceptance criteria

| ID | Given | When | Then |
|---|---|---|---|
| AC-001 | New email and valid password | Register | Account is created with hashed password and USER role |
| AC-002 | Valid credentials | Login | JWT contains user identity and role; password is absent |
| AC-003 | USER token | Call admin endpoint | 403 and no state change |
| AC-004 | Valid event and available venue | Create | Event is persisted with auditable actor and status |
| AC-005 | Two simultaneous last-seat requests | Register | At most one succeeds; other receives capacity conflict |
| AC-006 | Existing active registration | Register same event | Duplicate request is rejected or idempotently returns existing result |
| AC-007 | Cancelled event | Register | Request is rejected |
| AC-008 | Policy has matching chunks | Ask question | Answer cites document/chunk sources |
| AC-009 | No matching evidence | Ask policy question | Assistant declines to invent an answer |
| AC-010 | Destructive request without confirmation | Run agent | Assistant asks for confirmation and does not call tool |

