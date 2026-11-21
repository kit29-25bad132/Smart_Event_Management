# Agent tools

| Tool | Input | Output | Authorization |
|---|---|---|---|
| `search_events` | query, filters, pagination | event summaries | USER/ADMIN |
| `create_event` | title, times, venue, capacity | event | ADMIN + confirmation if policy requires |
| `update_event` | event ID, patch | event | ADMIN |
| `cancel_event` | event ID, reason, confirmation | cancelled event | ADMIN + explicit confirmation |
| `check_venue_availability` | venue ID, time range | availability/conflicts | USER/ADMIN |
| `register_participant` | event ID, participant | registration | self for USER; ADMIN may act for user |
| `cancel_registration` | registration ID, confirmation | cancelled registration | owner/ADMIN + confirmation |
| `get_event_details` | event ID | event details | USER/ADMIN |
| `search_event_policy` | question, filters | grounded passages/citations | USER/ADMIN |

Each schema rejects unknown fields, validates IDs/times, and returns typed success or stable error code. Tools call business services only.

