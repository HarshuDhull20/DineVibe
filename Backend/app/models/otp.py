from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.base import Base


# -------------------------
# ENUMS
# -------------------------

class OTPChannel(str, enum.Enum):
    SMS = "sms"
    EMAIL = "email"


class OTPPurpose(str, enum.Enum):
    LOGIN = "login"
    SIGNUP = "signup"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_RECOVERY = "account_recovery"
    PHONE_VERIFICATION = "phone_verification"


# -------------------------
# OTP MODEL
# -------------------------

class OTP(Base):
    """
    Stores OTPs for authentication & recovery flows.
    """

    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)

    # Link OTP to user (nullable for pre-signup OTPs)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    # Phone or Email where OTP was sent
    destination = Column(String, nullable=False)

    # Channel used
    channel = Column(Enum(OTPChannel), nullable=False)

    # Why this OTP exists
    purpose = Column(Enum(OTPPurpose), nullable=False)

    # Hashed OTP value
    otp_hash = Column(String, nullable=False)

    # Verification status
    is_verified = Column(Boolean, default=False)

    # Attempt counter (rate limiting)
    attempts = Column(Integer, default=0)

    # Expiry timestamp
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="otps")
