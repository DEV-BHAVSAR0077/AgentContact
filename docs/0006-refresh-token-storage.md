# ADR 0006: Refresh Token Storage

## Status
Accepted

## Context
We need a robust authentication system supporting short-lived access tokens (JWT) and long-lived refresh tokens. The refresh tokens must be securely stored and revocable to protect against token theft and session hijacking.

## Decision
We will store refresh tokens as hashed values (Argon2id) in the database within a `RefreshTokens` table associated with the `User`. The client will receive the raw refresh token via an `HttpOnly`, `Secure`, `SameSite=Strict` cookie.

1. **Format**: The refresh token is a high-entropy random string (e.g., UUIDv4 or `secrets.token_urlsafe(64)`).
2. **Storage**: The backend only stores the Argon2id hash of the refresh token.
3. **Revocation**: Deleting the row in the database instantly revokes the session.
4. **Expiry**: Database rows have an explicit `expires_at` column.

## Consequences
- **Positive**: High security against database dumps (refresh tokens cannot be reversed). Explicit session revocation is possible.
- **Negative**: Slight overhead of Argon2 verification during the token refresh flow. Requires a periodic cleanup task to delete expired tokens from the DB.
