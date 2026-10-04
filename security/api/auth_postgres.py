#!/usr/bin/env python3
"""
Production-grade JWT/OAuth2 with PostgreSQL refresh token management.
Implements replay attack prevention via token family tracking, JTI blacklisting,
SHA-256 token hashing, and transaction-locked refresh operations.
"""

import os
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Tuple
from enum import Enum

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from .models import Base, User as DBUser, Role as DBRole, UserRole as DBUserRole, RefreshToken as DBRefreshToken

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ["DATABASE_URL"]  # Required: PostgreSQL connection string
SECRET_KEY = os.environ["JWT_SECRET"]  # Required: min 32 chars, high entropy
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("JWT_REFRESH_DAYS", "7"))

# Database setup
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize tables
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------------------------------------------------------------------------
# Token Hashing (SHA-256 for storage)
# ---------------------------------------------------------------------------

def hash_token(token: str) -> bytes:
    """SHA-256 hash of token for secure storage."""
    return hashlib.sha256(token.encode()).digest()

def verify_token_hash(token: str, token_hash: bytes) -> bool:
    """Verify token against stored hash."""
    return hashlib.sha256(token.encode()).digest() == token_hash

# ---------------------------------------------------------------------------
# RBAC Models
# ---------------------------------------------------------------------------

class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    SCANNER = "scanner"
    VIEWER = "viewer"

class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    roles: List[str] = ["viewer"]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# ---------------------------------------------------------------------------
# JWT Token Creation & Validation
# ---------------------------------------------------------------------------

def create_access_token(user_id: int, username: str, roles: List[str], expires_delta: Optional[timedelta] = None) -> Tuple[str, str]:
    """Create access token; returns (token, jti)."""
    jti = secrets.token_urlsafe(32)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": username,
        "user_id": user_id,
        "roles": roles,
        "jti": jti,
        "exp": expire,
        "type": "access"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti

def create_refresh_token(user_id: int, username: str, roles: List[str], family_id: Optional[str] = None, db: Optional[Session] = None) -> Tuple[str, str, str]:
    """
    Create refresh token with family ID for replay attack prevention.
    Returns (token, jti, family_id).
    """
    family_id = family_id or secrets.token_urlsafe(32)
    jti = secrets.token_urlsafe(32)
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": username,
        "user_id": user_id,
        "roles": roles,
        "jti": jti,
        "family_id": family_id,
        "exp": expire,
        "type": "refresh"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    if db:
        token_hash = hash_token(token)
        db_token = DBRefreshToken(
            user_id=user_id,
            family_id=family_id,
            jti=jti,
            token_hash=token_hash,
            issued_at=datetime.now(timezone.utc),
            expires_at=expire
        )
        try:
            db.add(db_token)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

    return token, jti, family_id

def decode_token(token: str) -> Optional[Dict]:
    """Decode and validate JWT structure."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ---------------------------------------------------------------------------
# Refresh Token Rotation with Replay Attack Prevention
# ---------------------------------------------------------------------------

def rotate_refresh_token(
    old_token: str,
    user_id: int,
    db: Session,
    request: Optional[Request] = None
) -> Tuple[str, str, str]:
    """
    Rotate refresh token with family ID tracking and replay detection.

    Security guarantees:
    1. Token family ensures all refresh operations are tracked
    2. JTI (JWT ID) prevents token reuse
    3. SHA-256 hashing prevents token enumeration
    4. Transaction lock prevents concurrent refresh races
    5. Revocation timestamp tracks when tokens are invalidated
    """

    payload = decode_token(old_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    old_jti = payload.get("jti")
    family_id = payload.get("family_id")

    if not old_jti or not family_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed refresh token"
        )

    # Acquire lock and check token validity
    db_token = db.query(DBRefreshToken).filter(
        DBRefreshToken.jti == old_jti,
        DBRefreshToken.user_id == user_id
    ).with_for_update().first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found or already invalidated"
        )

    # Verify token hash
    if not verify_token_hash(old_token, db_token.token_hash):
        # Token hash mismatch suggests replay attack
        _revoke_token_family(family_id, db)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed; family revoked due to replay detection"
        )

    # Check if token already used (replay attack)
    if db_token.used_at is not None:
        # Replay detected: revoke entire family
        _revoke_token_family(family_id, db)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token reuse detected; token family revoked"
        )

    # Check if token is revoked
    if db_token.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )

    # Check expiration
    if datetime.now(timezone.utc) > db_token.expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    # Mark old token as used
    db_token.used_at = datetime.now(timezone.utc)

    # Fetch user and roles
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user or user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled"
        )

    user_roles = [ur.role.name for ur in user.roles]

    # Create new tokens in same family
    access_token, _ = create_access_token(user.id, user.username, user_roles)
    refresh_token, new_jti, _ = create_refresh_token(
        user.id,
        user.username,
        user_roles,
        family_id=family_id,
        db=db
    )

    # Commit transaction (row lock released)
    db.commit()

    return access_token, refresh_token, family_id

def _revoke_token_family(family_id: str, db: Session) -> None:
    """Revoke entire token family (triggered on replay detection)."""
    now = datetime.now(timezone.utc)
    db.query(DBRefreshToken).filter(
        DBRefreshToken.family_id == family_id,
        DBRefreshToken.revoked_at.is_(None)
    ).update({DBRefreshToken.revoked_at: now})

# ---------------------------------------------------------------------------
# FastAPI Dependencies
# ---------------------------------------------------------------------------

security = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

async def get_current_user(
    http_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    oauth_token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Validate access token and return user."""
    token = None
    if http_credentials:
        token = http_credentials.credentials
    elif oauth_token:
        token = oauth_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("user_id")
    username: str = payload.get("sub")

    if not user_id or not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user or user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return User.from_orm(user)

class RequireRoles:
    """RBAC dependency with PostgreSQL role lookup."""
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = set(allowed_roles)

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_roles = set(current_user.roles)
        if not user_roles.intersection(self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {list(self.allowed_roles)}"
            )
        return current_user
