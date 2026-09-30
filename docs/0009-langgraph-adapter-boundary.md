# ADR 0009: LangGraph Adapter Boundary

## Status
Accepted

## Context
AgentFlow defines a visual workflow using a generic Node/Edge JSON structure. LangGraph requires a specific `StateGraph` compilation step in Python. We need a way to dynamically map arbitrary visual graphs into LangGraph state machines.

## Decision
We will build a `GraphEngine` facade that reads the canonical `workflow_snapshot`. 
For V1, we implement a `NativeGraph` engine that manually resolves nodes topologically. 
In the future, a `LangGraphAdapter` will parse the snapshot, dynamically construct a `StateGraph`, compile it, and run it. The boundary is strictly the `workflow_snapshot` JSON schema.

## Consequences
- The frontend does not need to know about LangGraph.
- Backend can hot-swap execution engines.
