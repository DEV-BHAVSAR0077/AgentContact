# ADR 0003: Queue Technology (arq vs Celery)

## Status
Accepted

## Context
Workflow executions can take minutes. Processing them synchronously in FastAPI blocks the event loop. We need an asynchronous job queue.

## Decision
We will use **arq** (Async Redis Queue) in production because our codebase is heavily reliant on `asyncio` and `arq` is native to it, whereas Celery is synchronous by default.
For local development, we will use `asyncio.create_task` combined with strict try/except blocks to simulate background workers without requiring a local Redis instance.

## Consequences
- Requires Redis for production environments.
- Simpler `async` integration compared to Celery.
