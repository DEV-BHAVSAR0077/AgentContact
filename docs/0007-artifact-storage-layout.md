# ADR 0007: Artifact Storage Layout

## Status
Accepted

## Context
AgentFlow allows users to upload custom AI models (e.g. `.pkl`, `.joblib`) which are executed during a workflow. Initially, the backend simply mocked these uploads (setting status to `READY` without persisting files). To support a real sandbox environment (Phase 5), the backend must safely persist, validate, and retrieve these models. 

## Decision
We will implement local artifact storage as a preliminary step, abstracting it in a way that allows easy replacement with S3 or GCS.

1. **Storage Path**: `backend/artifacts/models/<model_id>/<checksum>_<filename>`.
2. **Streaming**: Files will be saved using `aiofiles` to prevent blocking the event loop on large model uploads.
3. **Validation**: A SHA-256 checksum will be calculated on-the-fly as the stream is saved to disk to verify integrity and detect tampering.
4. **Database State**: The `Model` table `file_path` will store the relative artifact path. The DB status will transition from `UPLOADING` to `READY` only if the checksum succeeds.

## Consequences
- Requires `aiofiles` dependency.
- Local artifact directory must be added to `.gitignore` and `.dockerignore`.
- We need to ensure that filename sanitization is enforced to prevent directory traversal attacks (e.g., rejecting `../../file.pkl`).
