# ADR 0005: Sandbox Pooling Strategy

## Status
Accepted

## Context
Starting a new Docker container for every single execution of a graph node introduces unacceptable latency (often 1-2 seconds per node).

## Decision
We will NOT implement warm container pooling for V1.
Instead, we will rely on process-level isolation for now, and accept the startup penalty of Docker containers if used. For workflows requiring fast inference, users should use the API integrations (`source_type="api"`) rather than uploading raw model weights.

## Consequences
- Slower execution times for uploaded artifacts.
- Simpler backend architecture (no pool manager needed).
