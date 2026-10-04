#!/usr/bin/env python3
"""
FastAPI authentication routes with PostgreSQL-backed refresh token rotation.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth_postgres import (
    get_db, get_current_user, RequireRoles,
    create_access_token, create_refresh_token, rotate_refresh_token,
    verify_password, User, Token, Role
)
from .models import User as DBUser, Role as DBRole, UserRole as DBUserRole

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

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
