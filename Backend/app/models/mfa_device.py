from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class MFADevice(Base):
    __tablename__ = "mfa_devices"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # MFA secret (TOTP)
    secret = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_used_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        "User",
        back_populates="mfa_devices"
    )
