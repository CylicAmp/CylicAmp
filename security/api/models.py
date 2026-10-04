"""
Database models for JWT/OAuth2 with PostgreSQL persistence.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, LargeBinary, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_username", "username"),
        Index("ix_users_disabled", "disabled"),
    )


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    # Relationships
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

    __table_args__ = (
        Index("ix_user_roles_user_id", "user_id"),
        Index("ix_user_roles_role_id", "role_id"),
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    family_id = Column(String(255), nullable=False, index=True)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    token_hash = Column(LargeBinary(32), nullable=False, unique=True, index=True)
    issued_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    used_at = Column(DateTime(timezone=True), nullable=True, index=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index("ix_refresh_tokens_user_id", "user_id"),
        Index("ix_refresh_tokens_family_id", "family_id"),
        Index("ix_refresh_tokens_expires_at", "expires_at"),
        Index("ix_refresh_tokens_revoked_at", "revoked_at"),
    )
