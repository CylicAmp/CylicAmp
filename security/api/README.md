# SecureScope API Authentication Module

Production-grade JWT/OAuth2 authentication with PostgreSQL-backed refresh token management, replay attack prevention, and role-based access control (RBAC).

## Architecture

### Security Layers

1. **Access Tokens (Short-lived, 15 minutes)**
   - JWT format: `{sub, user_id, roles, jti, exp, type}`
   - Stateless validation
   - Fast, no database lookup required
   - Contains `jti` (JWT ID) for revocation tracking

2. **Refresh Tokens (Long-lived, 7 days)**
   - Stored securely in PostgreSQL
   - SHA-256 hashed (never stored plaintext)
   - Token family ID for replay detection
   - Atomic rotation with transaction locks
   - Revocation timestamps track invalidation

3. **Replay Attack Prevention**
   - **Token Family Tracking**: All refresh tokens in a family are tracked together
   - **JTI Uniqueness**: Every token has a unique identifier
   - **Used-At Timestamps**: Track when tokens are consumed
   - **Family Revocation**: If a token is used twice (replay detected), entire family is revoked
   - **Transaction Locks**: Database row locks prevent concurrent refresh races

4. **Password Security**
   - bcrypt hashing with configurable rounds
   - Passlib integration for strength verification
   - Never stored or logged in plaintext

### Database Schema

```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    disabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255)
);

-- User-Role Mapping
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE
);

-- Refresh Tokens (secure storage with SHA-256 hashes)
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    family_id VARCHAR(255) NOT NULL,           -- Token family for replay detection
    jti VARCHAR(255) UNIQUE NOT NULL,          -- JWT ID
    token_hash BINARY(32) UNIQUE NOT NULL,     -- SHA-256 hash
    issued_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE,          -- When token was rotated
    revoked_at TIMESTAMP WITH TIME ZONE,       -- When token was revoked
    ip_address VARCHAR(45),
    user_agent VARCHAR(500)
);

-- Indexes for performance
CREATE INDEX ON refresh_tokens(user_id);
CREATE INDEX ON refresh_tokens(family_id);
CREATE INDEX ON refresh_tokens(expires_at);
CREATE INDEX ON refresh_tokens(revoked_at);
```

## Usage

### Installation

```bash
pip install -r security/api/requirements.txt
```

### Environment Variables

```bash
export DATABASE_URL="postgresql://user:password@localhost/securescope"
export JWT_SECRET="your-production-secret-key-min-32-chars"
export JWT_EXPIRE_MINUTES="15"
export JWT_REFRESH_DAYS="7"
```

### FastAPI Integration

```python
from fastapi import FastAPI
from security.api import auth_router

app = FastAPI()
app.include_router(auth_router)
```

### API Endpoints

#### 1. Login / Issue Tokens
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

#### 2. Refresh / Rotate Tokens
```http
POST /auth/refresh
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** New access + refresh token pair (same format as above)

#### 3. Get Current User
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@securescope.local",
  "full_name": "Administrator",
  "disabled": false,
  "roles": ["admin", "analyst", "scanner", "viewer"]
}
```

#### 4. Role-Protected Endpoints
```http
POST /auth/admin-only
Authorization: Bearer <access_token>
```

Only users with `admin` role can access.

### RBAC Usage in Routes

```python
from fastapi import Depends
from security.api import RequireRoles, get_current_user, User

@app.post("/sensitive-operation")
async def sensitive_op(
    current_user: User = Depends(RequireRoles(["admin"]))
):
    return {"message": f"Executed by {current_user.username}"}
```

## Security Guarantees

### Replay Attack Prevention

**Scenario**: Attacker intercepts a refresh token and attempts to use it multiple times.

**Protection**:
1. First refresh rotates the token and marks it as `used_at = now()`
2. Second attempt detects `used_at != NULL` and revokes entire family
3. All subsequent refreshes with tokens in that family fail

**Implementation**: `rotate_refresh_token()` function in `auth_postgres.py` uses:
- `db.query(...).with_for_update()` — acquires row-level lock
- `if db_token.used_at is not None: _revoke_token_family()` — detects reuse
- Transaction commit releases lock atomically

### Token Hash Verification

**Why**: Plaintext token storage is vulnerable if database is compromised.

**Implementation**:
- Tokens are hashed with SHA-256 before storage
- Verification compares `sha256(incoming_token) == stored_hash`
- If hash doesn't match, entire family is revoked (indicates token tampering)

### Expiration Enforcement

**Access tokens**: JWT exp claim (stateless, validated on each request)
**Refresh tokens**: `expires_at` checked in database (prevents use of expired tokens)

### Role-Based Access Control (RBAC)

```python
RequireRoles(["admin"])          # Require admin role
RequireRoles(["scanner", "admin"]) # Require either scanner or admin
```

- Roles loaded from database on each access token validation
- Role changes take effect immediately (no caching)
- Disabled users are rejected at validation time

## Configuration Checklist

- [ ] Change `JWT_SECRET` to a production-grade 32+ character string
- [ ] Set `DATABASE_URL` to production PostgreSQL instance
- [ ] Create initial users and roles in database
- [ ] Hash production user passwords: `python -c "from security.api import get_password_hash; print(get_password_hash('yourpassword'))"`
- [ ] Set appropriate token expiration times for your use case
- [ ] Enable HTTPS/TLS for all authentication endpoints
- [ ] Monitor `refresh_tokens` table for `revoked_at` entries (indicates attack attempts)
- [ ] Implement audit logging for all authentication events

## Performance Considerations

- **Indexes on `refresh_tokens`**: `user_id`, `family_id`, `expires_at`, `revoked_at`
- **Token rotation**: Single database write + commit (atomic)
- **Access token validation**: No database call (JWT verification only)
- **Connection pooling**: SQLAlchemy `pool_pre_ping=True` ensures active connections

## Known Limitations

1. **Horizontal Scaling**: Token families are checked per-database. Distributed systems need shared PostgreSQL or Redis cache for JTI blacklist.
2. **Token Revocation**: Currently immediate within same database. Cross-datacenter propagation requires replication.
3. **Audit Trail**: `ip_address` and `user_agent` are stored but not enforced. Additional logging recommended.

## Testing

See `test_auth.py` for comprehensive test suite covering:
- Successful login and token issuance
- Replay attack detection and family revocation
- Expired token rejection
- Role-based access control enforcement
- Concurrent refresh races (transaction lock verification)
