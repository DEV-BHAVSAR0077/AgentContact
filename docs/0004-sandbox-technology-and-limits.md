# ADR 0004: Sandbox Technology and Limits

## Status
Accepted

## Context
Uploaded models (like `.pkl` files) execute arbitrary Python code upon loading. To safely run these models during workflow execution, we need high-security isolation. 

## Decision
1. **Production Target**: We will use Docker containers (with dropped capabilities and no network access) as the sandbox environment.
2. **Local Fallback**: Due to Docker daemon unavailability on some Windows development hosts, we will implement a Python `subprocess` fallback. This fallback provides process-level isolation and timeouts but *does not* provide strict security containment (no namespaces/cgroups on Windows).
3. **Execution Limits**: 
   - Timeout: 30 seconds per model execution.
   - Memory/CPU limits: Enforced via Docker in prod, unenforced in local fallback.

## Consequences
- Developers running locally without Docker are at risk if they upload malicious `.pkl` files.
- The `SandboxAdapter` will dynamically switch between Docker and Subprocess based on environment capabilities.
