# Agent overview

The assistant is an authenticated interface over business services, not a database copilot. LangGraph manages a typed state graph; the LLM proposes intent and tool arguments, while deterministic authorization, Pydantic validation and services decide whether work can happen.

