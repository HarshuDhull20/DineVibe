from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum as SQLAlchemyEnum,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.base import Base


# -------------------------------------------------
# USER ROLES (Python Enum)
# -------------------------------------------------
class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"      
    ADMIN = "admin"
    RESTAURANT_OWNER = "restaurant_owner"
    RESTAURANT_STAFF = "restaurant_staff"
    NORMAL_USER = "normal_user"
    INFLUENCER = "influencer"


# -------------------------------------------------
# USER MODEL
# -------------------------------------------------
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)

    # -------------------------------------------------
    #  Keep this temporarily (single-role support)
    # We will migrate later to full multi-role table
    # -------------------------------------------------
    role = Column(
        SQLAlchemyEnum(UserRole, name="user_roles"),
        nullable=False,
        default=UserRole.NORMAL_USER
    )

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)

    # ================================
    # FIRST LOGIN & PASSWORD CONTROL
    # ================================
    is_first_login = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=True)

    # ADD THIS FOR PASSWORD EXPIRY
    password_changed_at = Column(DateTime(timezone=True), nullable=True)

    # ================================
    # MFA
    # ================================
    mfa_method = Column(String, nullable=True)
    mfa_secret = Column(String, nullable=True)
    is_mfa_enabled = Column(Boolean, default=False)

    # ================================
    # LOGIN TRACKING
    # ================================
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String, nullable=True)
    last_login_country = Column(String, nullable=True)

    # Optional flexible data per role
    role_data = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ================================
    # RELATIONSHIPS
    # ================================
    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    otps = relationship(
        "OTP",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    mfa_challenges = relationship(
        "MFAChallenge",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    mfa_devices = relationship(
        "MFADevice",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


# Force registration of related models
from app.models.session import UserSession
from app.models.audit_log import AuditLog
from app.models.otp import OTP
from app.models.mfa import MFAChallenge
from app.models.mfa_device import MFADevice