# ADR 0002: Graph Storage and Versioning

## Status
Accepted

## Context
The previous implementation stored raw React Flow JSON (view-layer data) directly in the database. This tightly coupled the backend execution engine to the frontend rendering library, making the backend fragile and untyped. Furthermore, executing a workflow and later modifying it would invalidate the execution history.

## Decision
1. **Pydantic Graph Schema**: We will define strict Pydantic models for the backend graph: `AgentNode`, `ModelNode`, `Edge`. The frontend must translate React Flow JSON into this canonical schema before saving or executing.
2. **Database Storage**: The database will store the validated JSON (matching the Pydantic schema) rather than raw React Flow data.
3. **Execution Snapshots**: Rather than implementing complex immutable table versioning, every `Execution` will store a `workflow_snapshot` (a copy of the nodes and edges at the exact moment of execution). This guarantees that historical execution logs remain accurate even if the original workflow is edited or deleted.

## Consequences
- **Positive**: Complete separation of concerns between visual rendering and backend execution. Robust execution history.
- **Negative**: The frontend must implement a serialization/deserialization adapter to translate between React Flow and the backend Pydantic schema.
