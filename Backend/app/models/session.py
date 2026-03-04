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


class UserSession(Base):
    """
    Stores per-device login sessions.
    Enables multi-device login, session tracking,
    device logout, and global logout.
    """

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # --- Ownership ---
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # --- Token Management ---
    access_token_jti = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    refresh_token = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )

    # --- Device Info ---
    device_type = Column(String, nullable=False)  
    # web / android / ios

    device_name = Column(String, nullable=True)
    # Chrome on Windows, iPhone 15, Pixel 7

    ip_address = Column(String, nullable=False)

    location = Column(String, nullable=True)
    # City / Country resolved from IP

    user_agent = Column(String, nullable=True)

    # --- Session State ---
    is_active = Column(Boolean, default=True)

    last_activity_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # --- Relationship ---
    user = relationship("User", back_populates="sessions")
