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


# -----------------------------
# ENUMS
# -----------------------------

class MFAType(str, enum.Enum):
    SMS = "sms"
    EMAIL = "email"
    TOTP = "totp"


class MFAPurpose(str, enum.Enum):
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"
    ACCOUNT_RECOVERY = "account_recovery"
    ROLE_CHANGE = "role_change"


# -----------------------------
# MFA CHALLENGE MODEL
# -----------------------------

class MFAChallenge(Base):
    __tablename__ = "mfa_challenges"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    mfa_type = Column(
        Enum(MFAType),
        nullable=False
    )

    purpose = Column(
        Enum(MFAPurpose),
        nullable=False
    )

    # OTP code or temp token (hashed)
    code = Column(String, nullable=False)

    is_verified = Column(Boolean, default=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationship back to user
    user = relationship(
        "User",
        back_populates="mfa_challenges"
    )
