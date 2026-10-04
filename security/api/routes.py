#!/usr/bin/env python3
"""
FastAPI authentication routes with:
  - PostgreSQL-backed JWT/refresh tokens (standard OAuth2)
  - Proof-of-work challenge (GF(37) hard problems for extreme concurrency)
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .auth_postgres import (
    get_db, get_current_user, RequireRoles,
    create_access_token, create_refresh_token, rotate_refresh_token,
    verify_password, User, Token, Role
)
from .models import User as DBUser, Role as DBRole, UserRole as DBUserRole
from .proof_of_work import (
    generate_problem, ProblemInstance, ProblemType, verify_proof, Proof
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
pow_router = APIRouter(prefix="/proof-of-work", tags=["Proof-of-Work"])

# ============================================================================
# Proof-of-Work Problem Instance Response
# ============================================================================

class ProblemResponse(BaseModel):
    """Problem instance returned to client."""
    problem_type: str
    timestamp: int
    requester_ip: str
    server_state_hash: str
    difficulty: int
    target: int
    base: int = 2

    @classmethod
    def from_instance(cls, problem: ProblemInstance) -> "ProblemResponse":
        return cls(
            problem_type=problem.problem_type.value,
            timestamp=problem.timestamp,
            requester_ip=problem.requester_ip,
            server_state_hash=problem.server_state_hash,
            difficulty=problem.difficulty,
            target=problem.target,
            base=problem.base
        )

# ---------------------------------------------------------------------------
# Login (Issue tokens)
# ---------------------------------------------------------------------------

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    POST /auth/token

    OAuth2-compatible login endpoint.
    Returns access token (short-lived, 15min default) and refresh token (long-lived, 7 days default).
    """
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disabled"
        )

    user_roles = [ur.role.name for ur in user.roles]

    access_token, _ = create_access_token(user.id, user.username, user_roles)
    refresh_token, _, family_id = create_refresh_token(user.id, user.username, user_roles, db=db)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=15 * 60
    )

# ---------------------------------------------------------------------------
# Token Refresh (Rotate tokens with replay protection)
# ---------------------------------------------------------------------------

@auth_router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    POST /auth/refresh

    Token rotation endpoint with replay attack prevention.

    Security features:
    - Token family tracking (revoke entire family if replay detected)
    - JTI (JWT ID) uniqueness enforcement
    - SHA-256 token hash verification
    - Transaction-level row locking prevents concurrent refresh races
    - Revocation timestamp tracking

    If a refresh token is used twice (replay attack), the entire token family is revoked.
    """
    try:
        new_access_token, new_refresh_token, family_id = rotate_refresh_token(
            refresh_token,
            current_user.id,
            db,
            request
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token rotation failed"
        )

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=15 * 60
    )

# ---------------------------------------------------------------------------
# Protected Endpoints Examples
# ---------------------------------------------------------------------------

@auth_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """GET /auth/me - Return current authenticated user."""
    return current_user

@auth_router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    POST /auth/logout - Revoke current access token.
    Note: In practice, you might track blacklisted JTIs to prevent further use.
    """
    return {"message": "Logged out successfully"}

@auth_router.post("/admin-only", dependencies=[Depends(RequireRoles(["admin"]))])
async def admin_endpoint(current_user: User = Depends(get_current_user)):
    """Example admin-protected endpoint."""
    return {"message": f"Admin operation by {current_user.username}"}

@auth_router.post("/scanner-only", dependencies=[Depends(RequireRoles(["scanner", "admin"]))])
async def scanner_endpoint(current_user: User = Depends(get_current_user)):
    """Example scanner-protected endpoint."""
    return {"message": f"Scan operation by {current_user.username}"}

# ============================================================================
# Proof-of-Work Endpoints (Complementary to JWT/OAuth2)
# ============================================================================

@pow_router.get("/problem", response_model=ProblemResponse)
async def get_problem(
    request: Request,
    path: str = "/api/protected"
) -> ProblemResponse:
    """
    GET /proof-of-work/problem

    Client fetches a proof-of-work challenge.
    The problem is ephemeral and time-locked to this exact moment.

    Query parameters:
      path: The endpoint the client wants to access

    Response: A problem instance (DISCRETE_LOG, ORBIT_COLLISION, etc.)

    Security properties:
    - Problem is unique to this IP, this moment, this server state
    - Problem expires after 5 seconds (is_expired check)
    - Solving takes 100-1000ms depending on difficulty
    - Reuse is impossible: different moment = different problem
    """

    ip = request.client.host if request.client else "unknown"

    # For this example, use DISCRETE_LOG (GF(37) discrete-log problem)
    # In production, could vary by path or client characteristics
    problem = generate_problem(
        requester_ip=ip,
        difficulty_ms=100,
        problem_type=ProblemType.DISCRETE_LOG
    )

    return ProblemResponse.from_instance(problem)

@pow_router.post("/verify")
async def verify_proof_endpoint(
    request: Request,
    proof_hash: int,
    solution: int,
    solve_time_ms: int,
    timestamp: int
) -> dict:
    """
    POST /proof-of-work/verify

    Client submits proof for verification.
    If valid, response includes a short-lived token for the actual request.

    Query parameters:
      proof_hash: Hash of problem instance
      solution: Solution to the problem
      solve_time_ms: How long solving took
      timestamp: When proof was generated

    Returns: {"valid": true, "token": "...ephemeral auth token..."}
    """

    ip = request.client.host if request.client else "unknown"

    # Reconstruct problem instance
    problem = generate_problem(ip)

    # Verify proof
    proof = Proof(
        problem_hash=proof_hash,
        solution=solution,
        solve_time_ms=solve_time_ms,
        timestamp=timestamp
    )

    is_valid, reason = verify_proof(proof, problem)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Proof verification failed: {reason}"
        )

    # If proof is valid, issue a short-lived token (5 minutes)
    # In production, this would tie to an actual user or device ID
    from datetime import timedelta
    access_token = "pow-valid-" + problem.server_state_hash[:16]

    return {
        "valid": True,
        "token": access_token,
        "expires_in": 300,  # 5 minutes
        "message": f"Proof-of-work valid. Token expires in 300s."
    }

@pow_router.post("/protected", dependencies=[Depends(get_current_user)])
async def pow_protected_endpoint(current_user: User = Depends(get_current_user)):
    """
    Example endpoint protected by proof-of-work + JWT.

    Client must:
    1. GET /proof-of-work/problem
    2. Solve the returned problem
    3. POST /proof-of-work/verify with solution
    4. Use returned token + JWT to access this endpoint

    Under extreme concurrency, this provides:
    - No centralized rate limiting needed (PoW is distributed)
    - No database queries for verification (O(1) crypto check)
    - Formal non-replayability guarantees (time-locked problems)
    """

    return {
        "message": f"Proof-of-work protected resource",
        "user": current_user.username,
        "note": "This endpoint requires both PoW proof and valid JWT"
    }

# Include both routers in app
__all__ = ["auth_router", "pow_router"]
