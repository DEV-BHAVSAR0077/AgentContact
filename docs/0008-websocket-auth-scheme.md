# ADR 0008: WebSocket Auth Scheme

## Status
Accepted

## Context
Execution streams are broadcast over WebSockets. Browser clients often cannot send `Authorization: Bearer <token>` headers during the WebSocket handshake (`new WebSocket(url)`). 

## Decision
1. **Authentication**: We will accept a `token` query parameter during the initial WebSocket connection (`/api/v1/executions/{id}/stream?token=xyz`).
2. **Pub/Sub**: In production, we will use Redis Pub/Sub to distribute messages across multiple FastAPI worker nodes. For local single-process development, we utilize a simple in-memory `Dict` to map execution IDs to active WebSocket connections.

## Consequences
- The frontend must extract the JWT from its state/cookie and append it to the WS URL.
- Local dev does not require Redis.
