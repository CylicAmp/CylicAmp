#!/usr/bin/env python3
"""
JWT / OAuth2 Authentication for SecureScope API
Replaces simple API key with stateless JWT tokens.
Supports role-based access control (RBAC).
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List
from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SECRET_KEY = os.environ["JWT_SECRET"]  # Required: set in production environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("JWT_REFRESH_DAYS", "7"))

# ---------------------------------------------------------------------------
# Password Hashing
# ---------------------------------------------------------------------------

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------------------------------------------------------------------------
# RBAC Models
# ---------------------------------------------------------------------------

class Role(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    SCANNER = "scanner"      # Service account for automated scans
    VIEWER = "viewer"

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    roles: List[Role] = [Role.VIEWER]

class UserInDB(User):
    hashed_password: str

# ---------------------------------------------------------------------------
# User Database
# Note: This simple implementation is for reference/testing only.
# Use auth_postgres.py with a real PostgreSQL database for production.
# Test user credentials must be loaded from environment or test fixtures, not hardcoded.
# ---------------------------------------------------------------------------

def _load_test_users() -> Dict[str, UserInDB]:
    """Load test users from environment. Not for production."""
    # Example: set TEST_USERS='admin:hashed_pw,analyst:hashed_pw' in env
    # Or use a fixture file: load_from_json(os.environ.get("TEST_USERS_FILE"))
    return {}

_USERS_DB = _load_test_users()

def get_user(username: str) -> Optional[UserInDB]:
    return _USERS_DB.get(username)

# ---------------------------------------------------------------------------
# JWT Token Handling
# ---------------------------------------------------------------------------

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    roles: List[str] = []

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[Dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ---------------------------------------------------------------------------
# FastAPI Dependencies & RBAC Enforcement
# ---------------------------------------------------------------------------

security = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

async def get_current_user(
    http_credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    oauth_token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    """
    Validate JWT from either Authorization: Bearer header or OAuth2 scheme.
    """
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
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type: expected access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token: missing subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    return user

class RequireRoles:
    """
    RBAC dependency factory.
    Usage: Depends(RequireRoles([Role.ADMIN, Role.ANALYST]))
    """
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = set(allowed_roles)

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_roles = set(current_user.roles)
        if not user_roles.intersection(self.allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required roles: {[r.value for r in self.allowed_roles]}"
            )
        return current_user

# ---------------------------------------------------------------------------
# Auth Router Example
# ---------------------------------------------------------------------------

from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
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

    token_payload = {
        "sub": user.username,
        "roles": [r.value for r in user.roles]
    }
    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@auth_router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")
    user = get_user(username)
    if not user or user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User invalid or disabled"
        )

    token_payload = {
        "sub": user.username,
        "roles": [r.value for r in user.roles]
    }
    new_access_token = create_access_token(token_payload)
    new_refresh_token = create_refresh_token(token_payload)

    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
