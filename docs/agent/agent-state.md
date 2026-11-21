# Agent state

State fields: `session_id`, authenticated `user_id`, `role`, conversation summary, latest message, classified intent, extracted arguments, candidate tool, confirmation state, tool results, citations, errors, run ID and final response. Persist minimal redacted checkpoints in `agent_runs`; never trust state fields as authorization without reloading identity from the token.

