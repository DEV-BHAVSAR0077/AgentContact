# Implementation Plan - AgentFlow

## Work Breakdown

### Phase 1: Foundation, Config, Database, Migrations
- Focus: Hardening the core backend setup, setting up Alembic, updating SQLAlchemy to 2.x async.
- Defect Fixes: D2, D6, D7, D8, D10.

### Phase 2: Authentication, Authorization, and Secrets
- Focus: Multi-tenant JWT auth, Argon2id passwords, API Key encryption, Audit logs, and Rate limiting.
- Defect Fixes: D1, D7.

### Phase 3: Domain Model, Versioning, and Graph Schema
- Focus: Establishing proper entity relationships, graph schema via Pydantic instead of raw React Flow JSON.
- Defect Fixes: D4, D9.

### Phase 4: Artifact Storage, Upload Pipeline, Model Registry
- Focus: Actual file persistence for uploaded models, checksum validation, model registry.
- Defect Fixes: D3.

### Phase 5: Runtimes, Adapters, and the Sandbox
- Focus: High security isolation for uploaded artifacts (.pkl, .joblib) via Docker Sandbox. Strict execution limits.
- Risk: Cross-platform Docker functionality (Windows host vs Linux containers).

### Phase 6: Graph Validation, Workflow Engine, Messaging, Execution
- Focus: Replacing mock execution with a real queue-based worker engine, building LangGraph & NativeGraph engines.
- Defect Fixes: D5.

### Phase 7: Real-Time Streaming
- Focus: WebSocket overhaul using Redis pub/sub for broadcast execution status updates.

### Phase 8: Frontend: Replace Every Mock With Real Behavior
- Focus: Connecting frontend with the hardened backend, integrating Zustand, strict typing, standard routing.
- Defect Fixes: D11.

### Phase 9: DevOps, CI/CD, Observability, Documentation
- Focus: Dockerizing all components, CI pipelines, README correction, Logging, Metrics.
- Defect Fixes: D12.

## ADRs to Write
- `0001-async-vs-sync-sqlalchemy.md`
- `0002-graph-storage-and-versioning.md`
- `0003-queue-technology-arq-vs-celery.md`
- `0004-sandbox-technology-and-limits.md`
- `0005-sandbox-pooling-strategy.md`
- `0006-refresh-token-storage.md`
- `0007-artifact-storage-layout.md`
- `0008-websocket-auth-scheme.md`
- `0009-langgraph-adapter-boundary.md`
- `0010-unsafe-format-policy.md`

## Open Questions
- Should SQLite fallback be fully disallowed outside tests, forcing Docker on all dev machines from Phase 1?
- What queue backends are readily accessible on the Windows host vs container boundary?

## Risks
- The frontend development server locking `.node` binary files (EPERM) during heavy task executions like `npm ci`.
- Running nested/sandbox Docker containers from a Windows dev environment with varying WSL2 permissions.
