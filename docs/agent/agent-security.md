# Agent security

Authenticated backend identity is authoritative; never accept a user ID inferred from text. Re-check RBAC in the tool and service. Treat prompts, retrieved documents and tool outputs as untrusted. Use allow-listed tools, schema validation, confirmation tokens bound to user/session/action, timeouts, retry limits, budget limits, audit records and redaction. Prompt injection cannot grant permissions or change system policy.

