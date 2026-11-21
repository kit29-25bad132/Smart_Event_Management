# Agent architecture

```mermaid
flowchart LR
 I[User intent] --> C[Classify/extract]
 C --> A{Authorized?}
 A -- no --> X[Refuse]
 A -- yes --> P[Plan in LangGraph]
 P --> T[Validated tool]
 T --> S[Business service]
 S --> D[(Database)]
 D --> R[Result node]
 R --> F[Final response]
```

LangGraph owns state, routing, retries and checkpoints. Tools are narrow adapters. Services enforce authorization again, validate domain invariants and transact. Confirmation is required before cancellation or other destructive state changes.

