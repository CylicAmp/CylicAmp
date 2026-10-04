"""
SecureScope API Security Module

Dual-authentication architecture:

1. PostgreSQL-backed JWT/OAuth2 (traditional, standards-compliant)
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (7 days) with family-based replay prevention
   - Role-based access control (RBAC)
   - Atomic token rotation with transaction-level locks

2. Proof-of-Work (GF(37) hard problems, novel research)
   - Ephemeral problems bound to time, IP, and server state
   - Discrete-log and orbit-collision challenges
   - O(1) verification with no database queries
   - Formally non-replayable under extreme concurrency
   - Complements JWT for rate limiting and DDoS resilience

Key modules:
  - auth_postgres: JWT/OAuth2 with PostgreSQL persistence
  - models: SQLAlchemy ORM (users, roles, refresh tokens)
  - routes: FastAPI endpoints (auth and proof-of-work)
  - proof_of_work: GF(37) challenge generation and verification
  - proof_of_work_client: Client-side solver library
"""

from .auth_postgres import (
    get_db,
    get_current_user,
    RequireRoles,
    create_access_token,
    create_refresh_token,
    rotate_refresh_token,
    User,
    Token,
    Role,
    verify_password,
    get_password_hash,
)
from .routes import auth_router, pow_router
from .models import Base
from .proof_of_work import (
    ProblemInstance,
    ProblemType,
    Proof,
    generate_problem,
    verify_proof,
    ServerState,
)
from .proof_of_work_client import ProofOfWorkClient

__all__ = [
    "auth_router",
    "pow_router",
    "get_db",
    "get_current_user",
    "RequireRoles",
    "create_access_token",
    "create_refresh_token",
    "rotate_refresh_token",
    "User",
    "Token",
    "Role",
    "verify_password",
    "get_password_hash",
    "Base",
    "ProblemInstance",
    "ProblemType",
    "Proof",
    "generate_problem",
    "verify_proof",
    "ServerState",
    "ProofOfWorkClient",
]
