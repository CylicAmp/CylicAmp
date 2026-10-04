"""
SecureScope API Security Module

Production-grade JWT/OAuth2 authentication with PostgreSQL-backed
refresh token management, replay attack prevention, and RBAC.

Key modules:
  - auth_postgres: Token creation, validation, and rotation with security
  - models: SQLAlchemy ORM models for users, roles, and refresh tokens
  - routes: FastAPI authentication endpoints
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
from .routes import auth_router
from .models import Base

__all__ = [
    "auth_router",
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
]
