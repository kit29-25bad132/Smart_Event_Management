# RAG specification

Supported initial formats: UTF-8 Markdown, TXT, HTML and PDF; ingestion is ADMIN/system-only and records MIME type, hash, source, version and status. Extract text, normalize, chunk by semantic/size boundaries with overlap, generate embeddings, and upsert versioned chunks into PostgreSQL pgvector. Query uses the same embedding model, metadata filters and similarity threshold; context includes source title/version/chunk index.

The generator must answer from retrieved evidence, cite sources, and say when evidence is insufficient. Updates create a new version; deletions disable retrieval and retain audit metadata. Embeddings and raw documents are provider/data-residency decisions, not Phase 1 implementations. Document text is data, never executable instructions.

