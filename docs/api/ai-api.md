# AI API

`POST /api/ai/sessions` authenticated creates session → 201. `POST /api/ai/sessions/{id}/messages` authenticated: `{message,confirmation_token?}` → 200 `{run_id,status,response,citations,tool_calls}`. `GET /api/ai/runs/{id}` owner/ADMIN → run status. `GET /api/admin/agent-activity` ADMIN → redacted activity. Every request is scoped to authenticated identity; destructive tools require confirmation. Recommended: streaming endpoint and feedback endpoint.

