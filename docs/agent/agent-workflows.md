# Agent workflows

```mermaid
sequenceDiagram
 participant U as User
 participant G as LangGraph
 participant T as Tool
 participant S as Service
 U->>G: request
 G->>G: classify/authorize/validate
 G->>T: typed call
 T->>S: business operation
 S-->>T: result/error
 T-->>G: redacted result
 G-->>U: final response + sources
```

Test scenarios: event search returns filters; event creation rejects USER and asks confirmation for ADMIN if destructive; registration handles full/duplicate/concurrent cases; cancellation requires confirmation; policy question cites evidence; hybrid search + policy performs bounded search then retrieval; unauthorized tool request is refused; ambiguous destructive request asks a clarifying confirmation.

