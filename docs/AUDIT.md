# Audit Report - AgentFlow

## Environment State
- Frontend: `npm ci`, `npm run build`, and `npm run lint` failed due to Windows locking `node_modules` (EPERM error from Vite running in the background, locking a tailwindcss binary). Consequently, `tsc` and `oxlint` could not be resolved.
- Backend: Dependencies frozen into `backend/requirements.txt`.

## Verified Defects
| ID | Defect | Severity | Evidence / Location | Proposed Fix |
|---|---|---|---|---|
| D1 | API keys leak | Critical | `models/db.py` and `POST /api/v1/models/` returning plaintext keys | Implement `SecretsProvider` with AES-256-GCM envelope encryption. Split schemas to remove key from read responses. |
| D2 | `temperature` type mismatch | Medium | `models/db.py` uses `Integer`, `schemas/domain.py` uses `float` | Alter column to `Float` in SQLAlchemy model and generate Alembic migration. |
| D3 | Upload is a mock | High | `api/endpoints/models.py` marks `READY` instantly with no file persistence | Implement `ArtifactStorage` local/S3 and async streaming file saving. |
| D4 | Workflow graph is raw React Flow JSON | High | `models/db.py` Workflow `nodes`/`edges` stored as pure JSON | Rebuild workflow schema using Pydantic; map frontend view to backend model. |
| D5 | Execution never fails cleanly | High | `api/endpoints/executions.py` WebSocket loop logic | Rewrite execution to run in isolated queue worker (`arq` / Redis); use Pub/Sub for WebSockets. |
| D6 | `Base.metadata.create_all()` runs in `main.py` | Medium | `backend/app/main.py` | Add Alembic for migrations; remove `create_all`. |
| D7 | Hardcoded default secrets & SQLite | High | `backend/app/core/config.py` | Use `pydantic-settings`; remove fallback secrets; mandate Postgres in prod. |
| D8 | `allow_origins=["*"]` + `allow_credentials=True` | High | `backend/app/main.py` | Provide explicit CORS origins from env var. |
| D9 | Deleting models creates orphans | Medium | `models/db.py` lacks FK restraints | Add FKs with `ON DELETE RESTRICT` via Alembic. |
| D10 | Deprecated APIs (orm_mode, utcnow) | Low | Spread throughout schemas/models | Replace with Pydantic v2 `from_attributes=True` and timezone-aware datetimes. |
| D11 | `/workflows` routes directly to builder; lacks lists | Medium | `frontend/src/App.tsx` | Implement proper React Router with distinct list/create/detail pages. |
| D12 | README claims capabilities that don't exist | Low | `README.md` | Rewrite README accurately in Phase 9. |
