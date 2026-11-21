# Observability architecture

Emit structured logs with request ID, user ID hash, agent session/run ID, tool-call ID, outcome and duration. Metrics cover API latency/error rate, registration conflicts, agent routing, tool failures, retrieval hit rate and token/cost budgets. Traces cross API → agent → tool → service. Redact passwords, JWTs, raw secrets and unnecessary personal data. Audit logs capture actor, action, target, outcome and timestamp.

